#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK service showing the RAID status of an IronPort Appliance.
"""
iport_raid_stat = {
    '1': 'Healthy(1)',
    '2': 'Failure(2)',
    '3': 'Rebuild(3)',
}

iport_map_raid_stat = {
    '1': 0,
    '2': 2,
    '3': 1,
}


def inventory_iport_raid(info):
    inventory = []

    if info:
        inventory = [(drive[0], None) for drive in info]

    return inventory


def check_iport_raid(item, _no_params, info):
    for drive in info:
        name, drvstat, lasterror = drive

        if name != item:
            continue

        msg = "Status: %s, Last error: %s" % (
            iport_raid_stat[drvstat], lasterror)

        return(iport_map_raid_stat[drvstat], msg)

    return(3, "no data found")


# pylint: disable=E0602
check_info['ironport_esa_raid'] = {
    "check_function": check_iport_raid,
    "inventory_function": inventory_iport_raid,
    "has_perfdata": False,
    "service_description": "IronPort RAID %s",
    "snmp_scan_function": ironport_snmp_scan,
    "snmp_info": (".1.3.6.1.4.1.15497.1.1.1.18.1", [
        3,  # raidID
        2,  # raidStatus
        4  # raidLastError
    ]),
    "includes": ["ironport.include"],
}
# pylint: enable=E0602
