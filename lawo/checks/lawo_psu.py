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

def check_lawo_psu(_no_item, _no_params, info):
    lawo_psu_map = {
        "1": "ok",
        "2": "notoperational",
    }
    
    state = 0
    psu1 = info[0][0]
    psu2 = info[0][1]

    psu1txt = lawo_psu_map[psu1]
    psu2txt = lawo_psu_map[psu2]

    psu1label = psu2label = ""

    if psu1 == "2":
        psu1label = "(!!)"
        state = 2
    if psu2 == "2":
        psu2label = "(!!)"
        state = 2

    return (state, "PSU1 Status is %s%s, PSU2 Status is %s%s" % (psu1txt, psu1label, psu2txt, psu2label))


check_info["lawo_psu"] = {
    'check_function'        : check_lawo_psu,
    'inventory_function'    : lambda info: len(info) > 0 and [(None, None)] or [],
    'service_description'   : "Lawo PSU",
    'has_perfdata'          : False,
    'snmp_info'             : (".1.3.6.1.4.1.14859.2.10.1.1", ["5.1", "6.1"]),
    'snmp_scan_function'    : lambda oid: oid(".1.3.6.1.2.1.1.2.0") in [".1.3.6.1.4.1.8072.3.2.10"] and oid(".1.3.6.1.4.1.14859.2.10.1.1.5.1"),
}

