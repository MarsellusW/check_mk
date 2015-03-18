#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2013             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

def inventory_epc_1200_port(info):
    info = info[0] if info[0] else info[1] if info[1] else None

    if not info:
        return []

    return [(line[0], None) for line in info]


def check_epc_1200_port(item, params, info):
    info = info[0] if info[0] else info[1] if info[1] else None

    if not info:
        return(3, 'no SNMP data found')

    for line in info:
        if line[0] == item:
            name, state, startup = line
            status = 0
            msg = 'current state "%s", configured startup state "%s"' % (\
                epc_1200_portstate[state], epc_1200_portstate[startup])

            if epc_1200_portstate[startup] == 'laststate':
                status = 1
            elif state != startup:
                status = 2

            return(status, msg)

    return(3, 'UNKNOWN - "%s" not found' % item)

check_info['gude_epc_1200_port'] = {
    'check_function'      : check_epc_1200_port,
    'inventory_function'  : inventory_epc_1200_port,
    'snmp_scan_function'  : epc_1200_snmp_scan,
    'service_description' : 'Port %s',
    'has_perfdata'        : False,
    'group'               : 'gude_epc_1200',
    'snmp_info'           : epc_1200_snmp_info['port'],
    'includes'            : ["gude_epc_1200.include"], }
