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
# from jujutranslator.nodetype2charm import Nodetype2Charm
from translator.toscalib.tosca_template import ToscaTemplate
import yaml
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper as Dumper

from pprint import pprint
from inspect import currentframe, getframeinfo


def usage():
    print 'juju-tosca-import.py [--help] [--description] <CSAR zip file>'


def description():
    print """Juju plugin to import a orchestration specification from
    a CSAR file containing YAML files"""


def unpack_zip(zipfn):
    # zip file needs to be in the TOSCA CSAR format
    # TODO This may be unnecessary if/when toscalib does it
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
    # Parse the TOSCA.meta file looking for yaml definitions
    # TODO This may be unnecessary if/when toscalib does it
    if not os.path.isfile(tmpdir+"/TOSCA-Metadata/TOSCA.meta"):
        print "TOSCA.meta not found in CSAR file"
        sys.exit(1)
    try:
        tfile = open(tmpdir+'/TOSCA-Metadata/TOSCA.meta', 'r')
    except:
        print "Couldn't open Tosca metafile"
        sys.exit(2)
    tlines = tfile.readlines()
    for line in tlines:
        if (line.startswith("Name")):
            attr, value = line.split(":", 2)
            # if it's a yaml file pointer, need to find it here, and parse it?
            logger.debug("Found yaml file: " + tmpdir + "/" + value.strip())
            # TODO Need to handle multiple yaml files
            tosca_tpl = os.path.join(tmpdir + "/" + value.strip())
            yamlcontent = ToscaTemplate(tosca_tpl)
            return yamlcontent


def create_charm(nodetmp, tmpdir, bundledir):
    # create a charm based on the node template
    logger.debug("Creating charm for:" + nodetmp.name + " " + nodetmp.type)
    # Make dirs and open files
    charmdir = bundledir + "/charms/" + nodetmp.name
    if not os.path.exists(charmdir):
        os.makedirs(charmdir)
    if not os.path.exists(charmdir + "/hooks"):
        os.makedirs(charmdir + "/hooks")
    configfn = charmdir + "/config.yaml"
    try:
        configfile = open(configfn, 'w')
    except:
        print ("Couldn't open config.yaml")
        sys.exit(2)
    metafn = charmdir + "/metadata.yaml"
    try:
        metafile = open(metafn, 'w')
    except:
        print ("Couldn't open metadata.yaml")
        sys.exit(2)
    metafile.write("Name: " + nodetmp.name + "\n")
    metafile.write("Summary: juju-tosca imported charm\n")
    metafile.write("Description: juju-tosca imported charm\n")

    # TODO: Write capabilities, provides & requires
    metafile.write("Provides:\n")
    for c in nodetmp.capabilities:
        metafile.write("  " + c.name + "\n")
    metafile.write("Requires:\n")
    # for r in nodetmp.requirements:
    #    print r
    #    metafile.write("  " + r.key + "\n")

    metafile.close()

    # Create the hooks
    for int in nodetmp.interfaces:
        if int.type == "tosca.interfaces.node.Lifecycle":
            if int.name == "configure":
                print("found config", int.name, int.implementation, int.input)
                configfile.write("options:\n")
                for key, val in int.input.items():
                    print "input: " + key
                    print val
                    configfile.write("  :" + key + "\n")
                    configfile.write("    default:\n")
                    configfile.write("    description: TOSCA imported option\n")
                    configfile.write("    type: string\n")
                # copy the script
                shutil.copy(tmpdir + "/" + int.implementation, charmdir + "/hooks/")
                # TODO create the juju wrapper script
            elif int.name == "start":
                print("found start", int.name, int.implementation, int.input)
            elif int.name == "create":
                print("found create", int.name, int.implementation, int.input)
            else:
                print(int.name, int.implementation, int.input)
    configfile.close()


def create_nodes(yaml, tmpdir, bundledir):
    # create node templates based on yaml file
    # tmpdir holds the contents of the CSAR file and may need
    # artifacts pulled from it.
    # bundledir is the output directory for the bundle file and
    # file artifacts should be placed there.
    cyaml = {}
    for nodetmp in yaml.nodetemplates:
        logger.debug("Found node type:" + nodetmp.name + " " + nodetmp.type)
        cyaml[nodetmp.name] = {}
        cyaml[nodetmp.name]['charm'] = nodetmp.name
        cyaml[nodetmp.name]['num_units'] = 1
        print "Props:" + str(sorted([p.name for p in nodetmp.properties]))
        print "Caps:" + str(sorted([p.name for p in nodetmp.capabilities]))

        if nodetmp.properties:
            cyaml[nodetmp.name]['options'] = {}
            for prop in nodetmp.properties:
                # TODO figure out proper mapping to bundle
                # TODO how to handle props that have get_input values?
                # This temporarily skips any "non-stringable" values
                if isinstance(prop.value, (basestring, int, float, long)):
                    cyaml[nodetmp.name]['options'][prop.name] = prop.value

        if nodetmp.requirements:
            cyaml[nodetmp.name]['constraints'] = {}
            for i in nodetmp.requirements:
                for req, node_name in i.items():
                    cyaml[nodetmp.name]['constraints'][req] = node_name

        create_charm(nodetmp, tmpdir, bundledir)
        # TODO not sure these classes are warranted with toscalib
        # doing the heavy lifting on the parser.
        # translator = Nodetype2Charm(nodetmp, bundledir)
        # translator.execute()
        print

    return(cyaml)


def create_relations(yaml, tmpdir, bundledir):
    ryaml = {}
    # create relations based on yaml file
    for nodetmp in yaml.nodetemplates:
        logger.debug("Found rel node:" + nodetmp.name + " " + nodetmp.type)
        for relation, node in nodetmp.relationship.items():
            ryaml[nodetmp.name] = node.name
    return(ryaml)


def create_bundle(byaml, bundledir):
    logger.debug(bundledir)
    bfn = bundledir + "/tosca.yaml"
    try:
        bfile = open(bfn, 'w')
    except:
        print ("Couldn't open bundlefile")
        sys.exit(2)
    bfile.write(yaml.safe_dump(byaml, default_flow_style=False, allow_unicode=True))
    bfile.close()
    return(bfn)


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

    # Read the TOSCA.meta file
    yaml = parse_metafile(tmpdir)

    # TODO should use this to mkdir, but its annoying right now
    # bundledir = tempfile.mkdtemp(prefix="BUNDLE_", dir="./")
    bundledir = "./BUNDLE"
    if not os.path.exists(bundledir):
        os.mkdir(bundledir)
    byaml = {'toscaImport': {}}
    cbundle = create_nodes(yaml, tmpdir, bundledir)
    byaml['toscaImport']['services'] = cbundle
    rbundle = create_relations(yaml, tmpdir, bundledir)
    byaml['toscaImport']['relations'] = rbundle
    bundlefile = create_bundle(byaml, bundledir)
    print "Import complete, bundle file is: " + bundlefile

    # cleanup tmpdir
    shutil.rmtree(tmpdir)
    # Should we clean up bundledir? On error only?
    # shutil.rmtree(bundledir)


if __name__ == "__main__":
    main()
