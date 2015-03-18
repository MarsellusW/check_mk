#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def check_fireeye_sysimage(_item, _params, info):
    if info:
        name, version_current, version_latest, is_latest = info[0]

        rc = 0

        label = ''
        version_status = 'is'

        is_latest = fireeye_truefalse[is_latest]

        if not is_latest:
            rc = 1

            version_status = 'is not'
            label = '(%s)(!)' % version_latest

        return rc, "Image %s, version %s latest available %s" % (name, version_status, label)
    else:
        return 3, "SysImage info not found in SNMP data"

check_info["fireeye_sysimage"] = {
    "check_function"      : check_fireeye_sysimage,
    "inventory_function"  : inventory_fireeye_generic,
    "has_perfdata"        : False,
    "service_description" : "FE SysImage",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.5.1", [ 1, 2, 3, 4 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include" ],
}

