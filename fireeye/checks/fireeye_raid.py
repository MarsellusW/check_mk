#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def check_fireeye_raid(_item, _params, info):
    if info:
        status, healthy = info[0]

        rc = 0

        label = ''
        msgtxt = 'healthy'
        healthy = fireeye_truefalse[healthy]

        if not healthy:
            rc = 1
            label = '(!)'
            msgtxt = 'un%s' % msgtxt

        return rc, "Raid is %s (\"%s\")%s" % (msgtxt, status, label)
    else:
        return 3, "RaidInfo not found in SNMP data"

check_info["fireeye_raid"] = {
    "check_function"      : check_fireeye_raid,
    "inventory_function"  : inventory_fireeye_generic,
    "has_perfdata"        : False,
    "service_description" : "FE Raid",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.2.1", [ 1, 2 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include" ],
}

