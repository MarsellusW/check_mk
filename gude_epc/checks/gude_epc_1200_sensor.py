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





epc_1200_humidity_default = (60, 70)
epc_1200_temp_default = (35, 40)
epc_1200_power_default = (10, 14)




def inventory_epc_1200_humidity(info):
    info = info[0] if info[0] else info[1] if info[1] else None

    if len(info) > 1:
        info = info[1]
    else:
        info = info[0]

    if len(info) > 0 and info[2] != "-9999":
        return [(None, "epc_1200_humidity_default")]

def check_epc_1200_humidity(_item, params, info):
    info = info[0] if info[0] else info[1] if info[1] else None

    if len(info) > 1:
        info = info[1]
    else:
        info = info[0]

    if len(info) > 0:
        value = int(info[2])
        value = value / 10.0

        warn, crit = params

        perfdata = [ ("humidity", value, warn, crit) ]

        msgtxt = "humidity is %.1f%% (levels at %d%%/%d%%)" % (\
                                                               value, warn, crit)

        state = 0

        if value == -999.9:
            state = 3
            msgtxt = "humidity data is unavailable"
        elif value >= crit:
            state = 2
        elif value >= warn:
            state = 1

        return(state, msgtxt, perfdata)

    return(3, 'HygroSensor not found')

check_info['gude_epc_1200_sensor.humidity'] = { # pylint: disable=E0602
    'check_function'      : check_epc_1200_humidity,
    'inventory_function'  : inventory_epc_1200_humidity,
    'snmp_scan_function'  : epc_1200_snmp_scan, # pylint: disable=E0602
    'service_description' : 'Humidity',
    'has_perfdata'        : True,
    'group'               : 'gude_epc_1200',
    'snmp_info'           : epc_1200_snmp_info['sensor'], # pylint: disable=E0602
    'includes'            : ["gude_epc_1200.include"],
}


def inventory_epc_1200_temp(info):
    info = info[0] if info[0] else info[1] if info[1] else None

    if len(info) > 1:
        info = info[1]
    else:
        info = info[0]

    if len(info) > 0 and info[1] != "-9999":
        return [(None, "epc_1200_temp_default")]

def check_epc_1200_temp(_item, params, info):
    info = info[0] if info[0] else info[1] if info[1] else None

    if len(info) > 1:
        info = info[1]
    else:
        info = info[0]

    if len(info) > 0:
        value = int(info[1])
        value = value / 10.0

        warn, crit = params

        perfdata = [ ("temp", value, warn, crit) ]

        msgtxt = "temperature is %.1f°C (levels at %d°/%d°)" % (value, warn, crit)

        state = 0

        if value == -999.9:
            state = 3
            msgtxt = "temperature data is unavailable"
        elif value >= crit:
            state = 2
        elif value >= warn:
            state = 1

        return(state, msgtxt, perfdata)

    return(3, 'TempSensor not found')

check_info['gude_epc_1200_sensor.temp'] = { # pylint: disable=E0602
    'check_function'      : check_epc_1200_temp,
    'inventory_function'  : inventory_epc_1200_temp,
    'snmp_scan_function'  : epc_1200_snmp_scan, # pylint: disable=E0602
    'service_description' : 'Temperature',
    'has_perfdata'        : True,
    'group'               : 'gude_epc_1200',
    'snmp_info'           : epc_1200_snmp_info['sensor'], # pylint: disable=E0602
    'includes'            : ["gude_epc_1200.include"],
}


# 20141121: beware the new firmware currently reports the powerchannel as not
#           active/valid, we take the value regardless of that

def inventory_epc_1200_power(info):
    info = info[0][0] if info[0] else info[1][0] if info[1] else None

    if len(info) > 0:
        return [(None, "epc_1200_power_default")]

def check_epc_1200_power(_item, params, info):
    info = info[0][0] if info[0] else info[1][0] if info[1] else None

    if len(info) > 0:
        value = int(info[0])
        value = value / 1000.0

        warn, crit = params

        perfdata = [ ("power", value, warn, crit) ]

        msgtxt = "power consumption is %.4fA (levels at %dA/%dA)" % (value, warn, crit)

        state = 0

        if value >= crit:
            state = 2
        elif value >= warn:
            state = 1

        return(state, msgtxt, perfdata)

    return(3, 'PowerSensor not found')

check_info['gude_epc_1200_sensor.power'] = { # pylint: disable=E0602
    'check_function'      : check_epc_1200_power,
    'inventory_function'  : inventory_epc_1200_power,
    'snmp_scan_function'  : epc_1200_snmp_scan, # pylint: disable=E0602
    'service_description' : 'Power Consumption',
    'has_perfdata'        : True,
    'group'               : 'gude_epc_1200',
    'snmp_info'           : epc_1200_snmp_info['sensor'], # pylint: disable=E0602
    'includes'            : ["gude_epc_1200.include"],
}
