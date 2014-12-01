#!/usr/bin/python
#
# Copyright 2014 IBM Corporation
# Liam Ji (jizilian@cn.ibm.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os

JUJU_RELATIONHOOKS = (RELATION_JOINED, RELATION_CHANGED,
                      RELATION_DEPARTED,
                      RELATION_BROKEN) = ('-relation-joined',
                                          '-relation-changed',
                                          '-relation-departed',
                                          '-relation-broken')

log = logging.getLogger('juju')

JUJU_CHARM_DIR_PERMISSION = \
    stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH
JUJU_HOOK_PERMISSION = \
    stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH
EXECUTE_SCRIPT_SUFFIX = "\.sh"

class RelationHooks():
    """
    This Class is used to translate to the relation hook in the Juju Charm
    There are three kinds of the relations in Juju
    a ) provides
    b ) requires
    c ) peers
    """

    def __init__(self, charm_dir, tosca_dir):
        """
        The constructor method
        :para charm_dir: the directory of Juju charm
        :para tosca_dir: the directory of TOSCA scripts
        """
        self.hook_dir = charm_dir + '/hooks'
        self.tosca_script_dir = tosca_dir

        if not os.path.exists(self.hook_dir):
            log.info("Create the Charm hooks directory.")
            os.makedirs(charm_dir, JUJU_CHARM_DIR_PERMISSION)

        if not os.path.exists(self.tosca_script_dir):
            log.warning("The TOSCA script directory doesn't exist.")
            raise Exception
    
    def _change_file_permission(self, file_path):
        """
        This method is used to change the file permission of the
        specified file
        :para file_path: the path of the file need to be changed
        :return 
        """
        os.chmod(file_path, JUJU_HOOK_PERMISSION)
    
    def _get_the_file_handle(self, need_create, file_path):
        """
        This method is used to get the handle of the specified file
        :para need_create: if need to create the new file, set as True;
                           otherwise set as False
        :para file_path: the path of the file
        :return file_handle: the file_handle of the specified file
        """
        file_handle = None
        if need_create:
            log.info("Create the relation hook file: %s.", file_path)
            file_handle = open(file_path, 'w')
        else:
            if not os.path.exists(self.hook_dir):
                log.warning("The TOSCA script: %s does not exist.", file_path)
                raise excepion
            else:
                file_handle =  open(file_path, 'r')
        return file_handle
        
    def map_relation_joined_hook(self, charm_name, tosca_script_path):
        """
        This method is used to generate the Juju [name]_relation_joined
        hook
        :para charm_name: the Juju Charm name
        :para tosca_script_path: the TOSCA script path
        :return
        """
        hook_name = charm_name + '-relation-joined'
        relation_hook_file = self.hook_dir + "/" + hook_name
        
        relation_hook_handle = self._get_the_file_handle(True, relation_hook_file)
        tosca_script_handle = self._get_the_file_handle(False, tosca_script_path)
        
        

        

    def map_relation_changed_hook(self, charm_name, tosca_script_path):
        """
        This method is used to generate the Juju [name]_relation_changed
        hook
        :para charm_name: the Juju Charm name
        :para tosca_script_path: the TOSCA script path
        :return
        """
        hook_name = charm_name + '-relation-changed'
        relation_hook_file = self.hook_dir + "/" + hook_name
        
        relation_hook_handle = self._get_the_file_handle(True, relation_hook_file)
        tosca_script_name = self._get_the_file_handle(False, tosca_script_path)


    def map_relation_departed_hook(self, charm_name, tosca_script_path):
        """
        This method is used to generate the Juju [name]_relation_departed
        hook
        :para charm_name: the Juju Charm name
        :parr tosca_script_path: the TOSCA script path
        :return
        """
        hook_name = charm_name + '-relation-departed'
        relation_hook_file = self.hook_dir + "/" + hook_name
        
        relation_hook_handle = self._get_the_file_handle(True, relation_hook_file)
        tosca_script_name = self._get_the_file_handle(False, tosca_script_path)

        

    def map_relation_broken_hook(self):
        """
        This method is used to generate the Juju [name]_relation_broken
        hook
        :para charm_name: the Juju Charm name
        :para tosca_script_path: the TOSCA script path
        :return
        """
        hook_name = charm_name + '-relation-broken'
        relation_hook_file = self.hook_dir + "/" + hook_name
        
        relation_hook_handle = self._get_the_file_handle(True, relation_hook_file)
        tosca_script_name = self._get_the_file_handle(False, tosca_script_path)
        
