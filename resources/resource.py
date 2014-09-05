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

class Resource(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._data = {}

    def set_item(self, name, value):
        if name not in self.SCHEMA:
            raise KeyError(_('"%s" is not valid item') % name)
        self._data[name] = value

    def get_item(self, name, defaultvalue=None):
        if name not in self.SCHEMA:
            raise KeyError(_('"%s" is not valid item') % name)
        return self._data.get(name, defaultvalue)

    def get_data(self):
        return self._data
