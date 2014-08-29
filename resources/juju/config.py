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

class Config(Resource):
    '''
    classdocs
    '''
    SCHEMA = (OPTIONS) = ('options')

#     def __init__(self):
#         '''
#         Constructor
#         '''
#         super(Config, self).__init__(cls.SCHEMA, {})

    def add_option(self, name, option):
        if self.get_item(self.OPTIONS) is None:
            self.set_item(self.OPTIONS, {})
        options = self.get_item(self.OPTIONS)
        options[name] = option

#         for name, info in data["options"].iteritems():
#                 for field, value in info.iteritems():
#                     if field == "type" 

class Option(Resource):
    '''
    classdocs
    '''
    SCHEMA = (TYPE, DEFAULT, DESCRIPTION) = ('type', 'default', 'description')
