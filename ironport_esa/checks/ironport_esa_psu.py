#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK service showing the of Power Supplies in an IronPort Appliance.
"""

state_label = {
    0: '',
    1: '(!)',
    2: '(!!)',
    3: '(!!!)',
}

ironport_psu_health_status = {
                              1: "not installed",
                              2: "healthy",
                              3: "no AC",
                              4: "faulty",
                              }

ironport_psu_state_map = {
                          }

def inventory_iport_psu(info):
    if info:
        return [(l[0], None) for l in info]
    else:
        return []


def check_iport_psu(item, _no_params, info):
    if info:
        for name, health, redundancy in info:
            if name == item:
                status = 0
                msg = []
                
                for type, value in [("Health", health), ("Redundancy", redundancy)]:
                    
                    msg.append("%s: %s" % (type, value, state_label[state]))
                    
                perfdata = [("health", health), ("redundancy", redundancy)]

        return(status, msg, perfdata)
    return(3, "no data found")


# pylint: disable=E0602
check_info['ironport_esa_psu'] = {
    "check_function": check_iport_psu,
    "inventory_function": inventory_iport_psu,
    "has_perfdata": True,
    "service_description": "IronPort PowerSupply %s",
    "snmp_scan_function": ironport_snmp_scan,
    "snmp_info": (".1.3.6.1.4.1.15497.1.1.1.8.1", [
        4,  # powerSupplyName
        2,  # powerSupplyStatus
        3  # powerSupplyRedundancy
    ]),
    "includes": ["ironport.include"],
}
# pylint: enable=E0602
