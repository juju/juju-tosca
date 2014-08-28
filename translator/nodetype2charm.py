#!/usr/bin/python

# Copyright 2014 IBM Corporation 
# Zhaizhixiang (zhzxzhai@cn.ibm.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from resources.tosca.node import Node
from resources.juju.metadata import Metadata
from resources.juju.metadata import Interface
from resources.juju.unithooks import UnitHooks
from resources.juju.config import Config, Option
from resources.resource import Resource
import os
import yaml
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper as Dumper
    
class Nodetype2Charm(object):
    '''
    classdocs
    '''
    TOSCA_OPERATIONS_TO_JUJU_HOOKS = {'create':'install', 'configure':'config-changed', 'start':'start',
                                      'stop':'stop', 'delete':'stop'}
    TOSCA_PROPERTY_TYPE_TO_JUJU_OPTION_TYPE = {'string':'string', 'integer':'int', 'float':'float',
                                               'boolean':'boolean', 'timestamp':'string'}
    METADATA_FILE_NAME = 'metadata.yaml'
    CONFIG_FILE_NAME = 'config.yaml'
    HOOKS_DIR_NAME = 'hooks'
    HOOKS_PERMISSION = 777 
    def __init__(self, name, nodetype, path):
        '''
        Constructor
        '''
        self._nodetype = nodetype
        self._name = name
        self._charm_path = path + '/' + name + '_charm'
        if os.path.isdir(self._charm_path):
            pass
        else:
            os.mkdir(self._charm_path)
        if os.path.isdir(self._charm_path + "/" + self.HOOKS_DIR_NAME):
            pass
        else:
            os.mkdir(self._charm_path + "/" + self.HOOKS_DIR_NAME)

    def execute(self):
        node = self._parse_node_type()
        metadata = self._translate_metadata(node)
        unithooks = self._translate_unithooks(node)
        config = self._translate_config(node)
        self._serialize_yaml(metadata, self._charm_path + "/" + self.METADATA_FILE_NAME)
        self._serialize_yaml(config, self._charm_path + "/" + self.CONFIG_FILE_NAME)
        self._serialize_hooks(unithooks, self._charm_path + "/" + self.HOOKS_DIR_NAME)

    def _serialize_yaml(self, resource, filepath):
        '''
          To serialize yaml object resource to file, such as meta.yaml, config.xml
        '''
        if isinstance(resource, Resource):
            with open(filepath, 'w') as outfile:
                outfile.write(yaml.dump(resource.get_data(), default_flow_style=False))

    def _serialize_hooks(self, hooks, path):
        operations = hooks.get_data()
        for k, v in operations.items():
            operation_file = path + '/' + k
            f = open(operation_file,'w')
            f.write(str(v))
            #os.chmod(operation_file, self.HOOKS_PERMISSION)
            f.close()

    def _parse_node_type(self): 
        node = Node(self._name, self._nodetype)
        return node

    def _translate_metadata(self, node):
        metadata = Metadata()
        metadata.set_item(Metadata.NAME, self._name)
        description = node.get_item(Node.DESCRIPTION)
        if description is not None:
            metadata.set_item(Metadata.DESCRIPTION, description)
        # FIXME: If we could mapping juju categories to tosca nodetype derived?.
#         derived = self._nodetype.get(Node.DERIVED_FROM)
#         if derived is not None:
#             if derived == self.TOSCA_SOFTWARE_COMPONENT:
#                 metadata.set_item(Metadata.CATEGORIES, Metadata.CATEGORIES_APPLICATIONS)
#             if derived == self.TOSCA_SOFTWARE_COMPONENT:
#                 metadata.set_item(Metadata.CATEGORIES, Metadata.CATEGORIES_APPLICATIONS)
        metadata.set_item(Metadata.CATEGORIES, Metadata.CATEGORIES_MISC)
        requirements = node.get_item(Node.REQUIREMENTS)
        if requirements is not None:
            for requirement in requirements:
                # Some requirements I don't know how to handle this, such as '*ubuntu_host' requirement.
                if isinstance(requirement, dict):
                    if requirement.get('host') is None:
                        name, interface = self._create_interface(requirement)
                        metadata.add_require(name, interface.get_data())
        capabilities = node.get_item(Node.CAPABILITIES)
        if capabilities is not None:
            for capability in capabilities:
                if capability.get('host') is None:
                    name, interface = self._create_interface(capability)
                    metadata.add_provide(name, interface.get_data())
        return metadata

    def _create_interface(self, relation):
        # FIXME: since the relation element of tosca is dict type, which means
        # it is not orderable, so I try to filter uncare attributes.
        interface = Interface()
        for k, v in relation.items():
            if k == 'host' or k == 'relationship_type' or k == 'interfaces':
                continue
            interface.set_item(Interface.INTERFACE, v)
            return k, interface

    def _translate_unithooks(self, node):
        hooks = UnitHooks()
        interfaces = node.get_item(Node.INTERFACES)
        if interfaces is not None:
            interface = interfaces.values()[0]
            for k, v in self.TOSCA_OPERATIONS_TO_JUJU_HOOKS.items():
                if interface.get(k) is not None:
                    hooks.set_item(v, interface.get(k))
        return hooks
    
    def _translate_config(self, node):
        config = Config()
        properties = node.get_item(Node.PROPERTIES)
        if properties is not None:
            for name, content in properties.items():
                    option = Option()
                    prop_type = content.get('type')
                    if prop_type is None:
                        #Assume the default type is string
                        prop_type = 'string'
                    option.set_item(Option.TYPE, self.TOSCA_PROPERTY_TYPE_TO_JUJU_OPTION_TYPE.get(prop_type))
                    default = content.get('default')
                    if default is not None:
                        option.set_item(Option.DEFAULT, default)
                    description = content.get('description')
                    option.set_item(Option.DESCRIPTION, description)
                    config.add_option(name, option.get_data())
        else:
            return None
        return config
