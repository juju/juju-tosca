#!/usr/bin/python
#
# Copyright 2014 IBM Corporation 
# Zhaizhixiang (zhzxzhai@cn.ibm.com)
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

from resources.resource import Resource


class Node(Resource):
    '''
    Charm class for translating tosca node_type to Juju charm
    '''

    SCHEMA = (DERIVED_FROM, DESCRIPTION, PROPERTIES, REQUIREMENTS,
            CAPABILITIES, INTERFACES, ARTIFACTS) = \
           ('derived_from', 'description', 'properties', 'requirements',
                     'capabilities', 'interfaces', 'artifacts')

    def __init__(self, node_name, data):
        '''
        Initialize the charm object from node name and node content
        '''
        super(Node, self).__init__()
        self._data = data
        self.node_name = node_name

    def get_name (self, node_name):
        '''
        Get charm name from the tosca node name
        '''
        #depends on the implementation, currently we just return the node name as charm name.
        #Maybe we will change the logic in the future.
        return node_name
