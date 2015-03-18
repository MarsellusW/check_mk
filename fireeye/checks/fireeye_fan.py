#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def inventory_fireeye_fan(info):
    if info:
        inventory = []

        for (name, status_txt, healthy, speed) in info:
            inventory.append((name, None))

        return inventory

def check_fireeye_fan(item, _params, info):
    for line in info:
        name, status_txt, healthy, speed = line

        if name == item:
            rc = 0

            label = ''
            msgtxt = 'healthy'
            healthy = fireeye_truefalse[healthy]
            speed = int(speed)

            if not healthy:
                rc = 1
                label = '(!)'
                msgtxt = "un%s" % msgtxt

            perfdata = [("rpm", speed)]

            return rc, "Fan %s is %s (\"%s\")%s, speed is %d rpm" % (name, msgtxt, status_txt, label, speed), perfdata

    return 3, "item not found in SNMP data"

check_info["fireeye_fan"] = {
    "check_function"      : check_fireeye_fan,
    "inventory_function"  : inventory_fireeye_fan,
    "has_perfdata"        : True,
    "service_description" : "FE Fan %s",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.4.1.3.1", [ 1, 2, 3, 4 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include" ],
}

