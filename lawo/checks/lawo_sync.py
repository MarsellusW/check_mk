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

def check_lawo_sync(_no_item, _no_params, info):
    lawo_sync_map = {
        "1": "multichannel",
        "2": "input1",
        "3": "input2",
        "4": "internal",
    }
    
    state = 0
    temp = info[0][0]

    if temp == "4":
        state = 2

    return (state, "Sync source is %s" % (lawo_sync_map[temp]))


check_info["lawo_sync"] = {
    'check_function'        : check_lawo_sync,
    'inventory_function'    : lambda info: len(info) > 0 and [(None, None)] or [],
    'service_description'   : "Lawo Sync Source",
    'has_perfdata'          : False,
    'snmp_info'             : (".1.3.6.1.4.1.14859.2.10.1.1.7", [1]),
    'snmp_scan_function'    : lambda oid: oid(".1.3.6.1.2.1.1.2.0") in [".1.3.6.1.4.1.8072.3.2.10"] and oid(".1.3.6.1.4.1.14859.2.10.1.1.7.1"),
}

