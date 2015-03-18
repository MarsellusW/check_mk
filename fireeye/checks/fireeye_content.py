#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

fireye_update_time_levels = (7200, 14400)

def check_fireeye_seccontent(_item, _params, info):
    if info:
        version, upd_passed, upd_time = info[0]

        fmt = '%Y/%m/%d %H:%M:%S'
        rc, label_d, timediff = cmp_time(upd_time, fmt, fireye_update_time_levels)

        label_s = ''

        upd_passed = fireeye_update[upd_passed]

        if upd_passed != "passed":
            rc = max(rc, 1)
            label_s = '(!)'

        return rc, "SecurityContent Version %s, last update %s%s at %s%s" % (version, upd_passed, label_s, upd_time, label_d)
    else:
        return 3, "SecurityContent info not found in SNMP data"

check_info["fireeye_content"] = {
    "check_function"      : check_fireeye_seccontent,
    "inventory_function"  : inventory_fireeye_generic,
    "has_perfdata"        : False,
    "service_description" : "FE SecurityContent",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.5.1", [ 5, 6, 7 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include", "generic.include" ],
}

