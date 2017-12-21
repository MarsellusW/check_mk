#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK service showing the PowerSupply status of an IronPort Appliance.
"""

iport_power_stat = {
    '1': 'Not Installed((1)',
    '2': 'Healthy(2)',
    '3': 'No AC(3)',
    '4': 'Faulty(4)',
}

iport_map_power_stat = {
    '1': 1,
    '2': 0,
    '3': 1,
    '4': 2,
}

iport_power_redundancy_stat = {
    '1': 'OK(1)',
    '2': 'Lost(2)',
}

iport_map_power_redundancy_stat = {
    '1': 0,
    '2': 1,
}

label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}


def inventory_iport_power(info):
    inventory = []

    if info:
        inventory = [(supply[0], None) for supply in info]

    return inventory


def check_iport_power(item, _no_params, info):
    for supply in info:
        name, pstat, rstat = supply

        if name != item:
            continue

        psstat = iport_power_stat[pstat]
        redstat = iport_power_redundancy_stat[rstat]

        pstat = iport_map_power_stat[pstat]
        rstat = iport_map_power_redundancy_stat[rstat]

        status = max(pstat, rstat)

        msg = "Status: %s%s, Redundancy: %s%s" % (
            psstat, label[pstat], redstat, label[rstat])

        return(status, msg)

    return(3, "no data found")


# pylint: disable=E0602
check_info['ironport_esa_power'] = {
    "check_function": check_iport_power,
    "inventory_function": inventory_iport_power,
    "has_perfdata": False,
    "service_description": "IronPort Power %s",
    "snmp_scan_function": ironport_snmp_scan,
    "snmp_info": (".1.3.6.1.4.1.15497.1.1.1.8.1", [
        4,  # powerSupplyName
        2,  # powerSupplyStatus
        3  # powerSupplyRedundancy
    ]),
    "includes": ["ironport.include"],
}
# pylint: enable=E0602
