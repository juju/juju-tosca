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
from resources.resource import Resource
class Metadata(Resource):
    '''
    classdocs
    '''
    SCHEMA = (NAME, SUMMARY, DESCRIPTION, MAINTAINER,
             CATEGORIES, SUBORDINATE, PROVIDES, REQUIRES, PEERS) = \
             ('name', 'summary', 'description', 'maintainer',
             'categories', 'subordinate', 'provides', 'requires', 'peers')
    CATEGORIES_APPLICATIONS = 'applications'
    CATEGORIES_APP_SERVERS = 'app-servers'
    CATEGORIES_CACHE_PROXY = 'cache-proxy'
    CATEGORIES_DATABASES = 'databases'
    CATEGORIES_FILE_SERVERS = 'file-servers'
    CATEGORIES_MISC = 'misc'




    def __init__(self):
        '''
        Constructor
        '''
        super(Metadata, self).__init__(self.SCHEMA, {})
    
    def add_provide(self, name, interface):
        if self.get_item(self.PROVIDES) is None:
            self.set_item(self.PROVIDES, {})
        provides = self.get_item(self.PROVIDES) 
        provides[name] = interface

    def add_peer(self, name, interface):
        if self.get_item(self.PEERS) is None:
            self.set_item(self.PEERS, {})
        peers = self.get_item(self.PEERS, {})
        peers[name] = interface

    def add_require(self, name, interface):
        if self.get_item(self.REQUIRES) is None:
            self.set_item(self.REQUIRES, {})
        requires = self.get_item(self.REQUIRES, {})
        requires[name] = interface

class Interface(Resource):
    
    SCHEMA = (INTERFACE, LIMIT, SCOPE, OPTIONAL) = \
                    ("interface", "limit", "scope", "optional")
    SCOPE_GLOBAL = "global"
    SCOPE_CONTAINER = "container"

    def __init__(self):
        '''
        Constructor
        '''
        super(Interface, self).__init__(self.SCHEMA, {})
