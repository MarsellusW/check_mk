#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK service showing the Temperature status of an IronPort Appliance.
"""


def inventory_iport_temp(info):
    inventory = []

    if info:
        inventory = [(temp[0], None) for temp in info]

    return inventory


def check_iport_temp(item, _no_params, info):
    for temp in info:
        name, degree = temp

        if name != item:
            continue

        degree = int(degree)
        perfdata = [('temp', degree)]
        msg = "Current temperature: %d" % degree

        return(0, msg, perfdata)

    return(3, "no data found")


# pylint: disable=E0602
check_info['ironport_esa_temp'] = {
    "check_function": check_iport_temp,
    "inventory_function": inventory_iport_temp,
    "has_perfdata": True,
    "service_description": "IronPort Temperature %s",
    "snmp_scan_function": ironport_snmp_scan,
    "snmp_info": (".1.3.6.1.4.1.15497.1.1.1.9.1", [
        3,  # temperatureName
        2  # degreesCelsius
    ]),
    "includes": ["ironport.include"],
}
# pylint: enable=E0602
