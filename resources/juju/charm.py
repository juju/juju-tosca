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

class Charm(object):
    '''
    Charm class for Juju charm
    '''
    
    def __init__(self, meta, hooks, config):
        '''
        Constructor
        '''
        self.meta = meta
        self.hooks = hooks
        self.config = config


 
        