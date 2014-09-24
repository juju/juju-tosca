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


import getopt
import sys
import zipfile
import tempfile
import os.path
import logging
import shutil
from jujutranslator.nodetype2charm import Nodetype2Charm
from translator.toscalib.tosca_template import ToscaTemplate
import pprint
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


def unpack_zip(zipfn):
    # zip file needs to be in the TOSCA CSAR format
    try:
        zip = zipfile.ZipFile(zipfn, 'r')
    except:
        print "Unable to open zip file", zipfn
        usage()
        sys.exit(2)

    logger.debug(zip.namelist())
    tmpdir = tempfile.mkdtemp(prefix="CSAR_", dir="./")
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
            attr, value = line.split(":", 2)
            # if it's a yaml file pointer, need to find it here, and parse it?
            logger.debug("Found yaml file: " + tmpdir + "/" + value.strip())
            # Need to handle multiple yaml files
            tosca_tpl = os.path.join(tmpdir + "/" + value.strip())
            yamlcontent = ToscaTemplate(tosca_tpl)

            return yamlcontent


def create_charms(yaml, tmpdir, bundledir):
    # create charms based on yaml file
    # tmpdir holds the contents of the CSAR file and may need
    # artifacts pulled from it.
    # bundledir is the output directory for the bundle file and
    # file artifacts should be placed there.
    for nodetmp in yaml.nodetemplates:
        logger.debug("Found node type:" + nodetmp.name)
        #translator = Nodetype2Charm(nodetmp.name, nodetmp, bundledir)
        #translator.execute()

    return("bundle file data for charms")


def create_relations(yaml, tmpdir, bundledir):
    # create relations based on yaml file
    return("bundle file data for relations")


def create_bundle(bundle, bundledir):
    logger.debug(bundle)
    return("Bundlefilename")


# Main
def main():
    # setup debug logging
    global logger
    logger = logging.getLogger('root')
    # FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s()]%(message)s"
    FORMAT = "[%(lineno)s-%(funcName)s] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)

    # input params
    zipfn = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd", ["help", "description"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
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

    # Unpack the zip file into a temp directory
    zipfn = sys.argv[1]
    tmpdir = unpack_zip(zipfn)
    bundledir = tempfile.mkdtemp(prefix="BUNDLE_", dir="./")

    # Read the TOSCA.meta file
    yaml = parse_metafile(tmpdir)

    cbundle = create_charms(yaml, tmpdir, bundledir)
    rbundle = create_relations(yaml, tmpdir, bundledir)
    bundlefile = create_bundle(str(cbundle) + "\n" + str(rbundle), bundledir)
    print "Import complete, bundle file is: " + bundlefile

    # cleanup tmpdir
    shutil.rmtree(tmpdir)
    # Should we clean up bundledir? On error only?
    # shutil.rmtree(bundledir)


if __name__ == "__main__":
    main()
