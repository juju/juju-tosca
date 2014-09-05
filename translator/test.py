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
import os
import sys


POSSIBLE_TOPDIR = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir))
if os.path.exists(os.path.join(POSSIBLE_TOPDIR, 'translator', '__init__.py')):
    sys.path.insert(0, POSSIBLE_TOPDIR)

from nodetype2charm import Nodetype2Charm
import yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader
  
def main():
    
    yamlcontent=parse_yaml("./mongoCSAR/mongo-node-elk.yaml")
    for key,val in yamlcontent['node_types'].items():
        translator = Nodetype2Charm(key, val, '.')
        translator.execute()
    print "finished"
def parse_yaml(yamlfile):
  #open the yaml file, and load the content
  try:
    yf=open(yamlfile,"r")
  except:
    print "Unable to open yaml file", yamlfile
    sys.exit(1)

  content=yf.read()
  yc=yaml.load(content, Loader=Loader)
  return yc    
if __name__ == '__main__':
    main()
