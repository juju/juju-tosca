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

JUJU_RELATIONHOOKS = (RELATION_JOINED, RELATION_CHANGED,
                      RELATION_DEPARTED,
                      RELATION_BROKEN) = ('relation-joined',
                                          'relation-changed',
                                          'relation-departed',
                                          'relation-broken')

log = logging.getLogger('juju')


class RelationHooks():
    """
    This Class is used to translate to the relation hook in the Juju Charm
    """

    def __init__(self):
        pass

    def map_relation_joined_hook(self):
        """
        This method is used to generate the Juju [name]_relation_joined
        hook
        :para
        :return
        """

        pass

    def map_relation_changed_hook(self):
        """
        This method is used to generate the Juju [name]_relation_changed
        hook
        :para
        :return
        """

        pass

    def map_relation_departed_hook(self):
        """
        This method is used to generate the Juju [name]_relation_departed
        hook
        :para
        :return
        """

        pass

    def map_relation_broken_hook(self):
        """
        This method is used to generate the Juju [name]_relation_broken
        hook
        :para
        :return
        """
        pass
