#!/usr/bin/env python
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

gude_epc_4ds_power_default = (10, 14)

def inventory_gude_epc_4ds_power(info):
    if len(info) > 0:
        return [(None, "gude_epc_4ds_power_default")]

def check_gude_epc_4ds_power(_item, params, info):
    if len(info) > 0:
        value = int(info[0][0])
        value = value / 1000.0
        warn, crit = params

        perfdata = [ ("power", value, warn, crit) ]

        msgtxt = "power consumption is %.4fA (levels at %dA/%dA)" % (value, warn, crit)

        state = 0

        if value >= warn:
            state = 1
        if value >= crit:
            state = 2

        return(state, msgtxt, perfdata)

    return(3, 'PowerSensor not found')

check_info['gude_epc_4ds_power'] = {
    'check_function' : check_gude_epc_4ds_power,
    'inventory_function' : inventory_gude_epc_4ds_power,
    'snmp_scan_function' : lambda oid: oid(".1.3.6.1.2.1.1.1.0") in ["Expert Power Control 1200", "Expert Power Control 4x Desktop 1200"],
    'service_description' : 'Power Consumption',
    'has_perfdata' : True,
    'snmp_info' : ('.1.3.6.1.4.1.28507.11.1.3', [
                     '1',  # epc4dsIrms
                  ]),
}
