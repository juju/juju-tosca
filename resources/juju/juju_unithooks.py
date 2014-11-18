#!/usr/bin/python
#
# Copyright 2014 IBM Corporation
# Zhaizhixiang (zhzxzhai@cn.ibm.com)
# Ji Zi Lian (jizilian@cn.ibm.com)
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
import os
import shutil
import string
import stat

JUJU_UNITHOOKS = (INSTALL, CONFIG_CHANGED, START, UPGRADE_CHARM,
                  STOP) = ('install', 'config-changed',
                           'start', 'upgrade-charm',
                           'stop')

log = logging.getLogger('juju')

JUJU_CHARM_DIR_PERMISSION = \
    stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH
JUJU_HOOK_PERMISSION = \
    stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH
EXECUTE_SCRIPT_SUFFIX = "\.sh"


class UnitHooks():
    '''
    This class is used to translate to the unit hooks in the Juju Charm.
    Based on the current design:
    a) The CASR files will be translated to a Juju bundle.
    b) Each nodetype will be translated to a Juju charm.
    c) During translating the Juju charm, create a new instance of this
    class to translate the Juju unit hooks
    '''
    def __init__(self, charm_dir, tosca_dir):
        """
        The constructor method
        :para charmDir: the directory of Juju charm
        """
        self.hook_dir = charm_dir + '/hooks'
        self.tosca_script_dir = tmpdir

        if not os.path.exists(self.hook_dir):
            log.info("Create the Charm hooks directory.")
            os.makedirs(charm_dir, JUJU_CHARM_DIR_PERMISSION)

        if not os.path.exists(self.tosca_script_dir):
            log.warning("The TOSCA script directory doesn't exist.")
            raise Exception

    def _change_file_permission(self, file_path):
        """
        This method is used to change the file permission of hook
        :para file_path: the file path
        """
        os.chmod(file_path, JUJU_HOOK_PERMISSION)

    def map_install_hook(self, script_path):
        """
        This method is used to generate the install hook
        :para script_path: the absolute path of the TOSCA artifact script
        :result is_successful. If the install hook is created successfully,
        return True, otherwise False
        """
        is_successful = False

        script_path = self.tosca_script_dir + '/' + script_path

        if not os.path.exists(script_path):
            log.warning("Can not find the TOSCA \
                artifact file: %s.", script_path)
            return is_successful

        script_name = os.path.basename(script_path)
        if (script_name is None or
                not strchr(script_name, EXECUTE_SCRIPT_SUFFIX)):
            log.warning("Can not find the execute file: %s.", script_path)
            return is_successful

        src_path = script_path
        dst_path = self.hook_dir + '/' + 'install.sh'

        try:
            shutil.copy(src_path, dst_path)
        except Exception:
            pass

        if os.path.exists(dst_path):
            self._change_file_permission(dst_path)
            is_successful = True
        else:
            log.error("Could not find the install hook file.")

        return is_successful

    def map_config_changed_hook(self):
        """
        This method is used to generate the config changed hook
        :para
        :result
        """

    def map_start_hook(self, script_path):
        """
        This method is used to generate the start hook
        :para script_path: the absolute path of the TOSCA artifact script
        :result is_successful. If the install hook is created successfully,
        return True, otherwise False
        """
        is_successful = False

        script_path = self.tosca_script_dir + '/' + script_path

        if not os.path.exists(script_path):
            log.warning("Can not find the TOSCA \
                artifact file: %s.", script_path)
            return is_successful

        script_name = os.path.basename(script_path)
        if (script_name is None or
                not strchr(script_name, EXECUTE_SCRIPT_SUFFIX)):
            log.warning("Can not find the execute file: %s.", script_path)
            return is_successful

        src_path = script_path
        dst_path = self.hook_dir + '/' + 'start.sh'

        try:
            shutil.copy(src_path, dst_path)
        except Exception:
            pass

        if os.path.exists(dst_path):
            self._change_file_permission(dst_path)
            is_successful = True
        else:
            log.error("Could not find the start hook file.")

        return is_successful

    def map_update_charm_hook(self):
        """
        This method is used to generate the update charm hook
        :para
        :result
        """

    def map_stop_hook(self, script_path):
        """
        :para script_path: the absolute path of the TOSCA artifact script
        :result is_successful. If the install hook is created successfully,
        return True, otherwise False
        """
        is_successful = False

        script_path = self.tosca_script_dir + '/' + script_path

        if not os.path.exists(script_path):
            log.warning("Can not find the TOSCA \
                artifact file: %s.", script_path)
            return is_successful

        script_name = os.path.basename(script_path)
        if (script_name is None or
                not strchr(script_name, EXECUTE_SCRIPT_SUFFIX)):
            log.warning("Can not find the execute file: %s.", script_path)
            return is_successful

        src_path = script_path
        dst_path = self.hook_dir + '/' + 'stop.sh'

        try:
            shutil.copy(src_path, dst_path)
        except Exception:
            pass

        if os.path.exists(dst_path):
            self._change_file_permission(dst_path)
            is_successful = True
        else:
            log.error("Could not find the stop hook file.")

        return is_successful
