#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def check_fireeye_sysinfo(_item, _params, info):
    if info:
        status, model, serial = info[0]

        rc = 0

        label = ''

        if status != "Good":
            rc = 1
            label = '(!)'

        return rc, "HW-Model %s, SNR %s, Status is \"%s\"%s" % (model, serial, status, label)
    else:
        return 3, "SysInfo not found in SNMP data"

check_info["fireeye_sysinfo"] = {
    "check_function"      : check_fireeye_sysinfo,
    "inventory_function"  : inventory_fireeye_generic,
    "has_perfdata"        : False,
    "service_description" : "FE SysInfo",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.1.1", [ 1, 2, 3 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include" ],
}

