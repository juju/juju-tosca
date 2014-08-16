#!/usr/bin/python

# Copyright 2014 IBM Corporation 
# Michael Chase-Salerno(bratac@linux.vnet.ibm.com)

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


import yaml
import pprint
import getopt
import sys
import zipfile
import tempfile
import os.path
import logging
import shutil
from inspect import currentframe, getframeinfo

try:
  from yaml import CSafeLoader as Loader
except ImportError:
  from yaml import SafeLoader as Loader

def usage():
  print 'juju-tosca-import.py [--help] [--description] <CSAR zip file>'

def description():
  print """Juju plugin to import a orchestration specification from 
  a CSAR file containing YAML files"""

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
 
def unpack_zip(zipfn):
  #zip file needs to be in the TOSCA CSAR format
  try:
    zip = zipfile.ZipFile(zipfn, 'r') 
  except:
    print "Unable to open zip file", zipfn
    usage()
    sys.exit(2)
 
  logger.debug(zip.namelist())
  tmpdir=tempfile.mkdtemp(prefix="CSAR_", dir="./")
  zip.extractall(tmpdir)
  return tmpdir

def parse_metafile(tmpdir):
  if not os.path.isfile(tmpdir+"/TOSCA-Metadata/TOSCA.meta"):
    print "TOSCA.meta not found in CSAR file"
    sys.exit(1)
  tfile = open(tmpdir+'/TOSCA-Metadata/TOSCA.meta', 'r')
  tlines = tfile.readlines()
  for line in tlines:
    if (line.startswith("Name")):
      attr,value = line.split(":",2)
      # if it's a yaml file pointer, need to find it here, and parse it?
      logger.debug("Found yaml file: "+tmpdir+"/"+value.strip())
      # Need to handle multiple yaml files
      yamlcontent=parse_yaml(tmpdir+"/"+value.strip())
  return yamlcontent

def create_charm(name,spec):
  pass

def create_charms(yaml):
  #create charms based on yaml file
  for key,val in yaml['node_types'].items():
    logger.debug("Found node type:"+key)
    create_charm( key, val );
  #pprint.pprint(yaml['node_types'])

def create_relations(yaml):
  # create relations based on yaml file
  pass

def create_bundle():
  pass

#Main
def main():
  #setup debug logging  
  global logger
  logger = logging.getLogger('root')
  #FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s()]%(message)s"
  FORMAT = "[%(lineno)s-%(funcName)s] %(message)s"
  logging.basicConfig(format=FORMAT)
  logger.setLevel(logging.DEBUG)
   
  #input params
  zipfn=''
  yamlfile=''
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd", ["help", "description"])
  except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)

  for opt,arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-d", "--description"):
      description()
      sys.exit()
    else:
        assert False, "unhandled option"

  if not (len(args) == 1):
    usage()
    sys.exit(2)

  # Unpack the zip file into a tmp directory
  zipfn=sys.argv[1] 
  tmpdir=unpack_zip(zipfn)

  # Read the TOSCA.meta file
  yaml=parse_metafile(tmpdir)
#  logger.debug("Yaml content:")
#  pprint.pprint(yaml) 
  for t,val in yaml.items():
      logger.debug("Found yaml root item:"+t)
  
  create_charms(yaml)
  create_relations(yaml)
  create_bundle()
  
  #cleanup tmpdir
  shutil.rmtree(tmpdir)

if __name__ == "__main__":
  main()

