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
import sys

from translator.toscalib.utils.gettextutils import _


log = logging.getLogger('juju')


class TOSCAToJujuException(Exception):
    '''
    Base exception class for TOSCA-Juju translator tool.
    
    This class is used to describe the exception is meet during
    translating the TOSCA to Juju.
     
    The detailed exception exception inherits from this class.
    '''

    def __init__(self, **kwargs):
        self.message = self.msg_fmt % kwargs
        

    def __str__(self):
        return self.message

    
class MissingRequiredFile(TOSCAToJujuException):
    msg_fmt = _('The file %(what)s is missed')


