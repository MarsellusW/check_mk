#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def inventory_fireeye_psu(info):
    if info:
        inventory = []

        for (name, status_txt, healthy) in info:
            inventory.append((name, None))

        return inventory

def check_fireeye_psu(item, _params, info):
    for line in info:
        name, status_txt, healthy = line

        if name == item:
            rc = 0

            label = ''
            msgtxt = 'healthy'
            healthy = fireeye_truefalse[healthy]

            if not healthy:
                rc = 1
                label = '(!)'
                msgtxt = "un%s" % msgtxt

            return rc, "PowerSupply %s is %s (\"%s\")%s" % (name, msgtxt, status_txt, label)

    return 3, "item not found in SNMP data"

check_info["fireeye_psu"] = {
    "check_function"      : check_fireeye_psu,
    "inventory_function"  : inventory_fireeye_psu,
    "has_perfdata"        : False,
    "service_description" : "FE PowerSupply %s",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.3.1.3.1", [ 1, 2, 3 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include" ],
}

