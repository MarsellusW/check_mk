#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

fe_truefalse = {
                 "1": "true",
                 "2": "false",
               }

fe_update = {
              "1": "passed",
              "2": "failed",
            }

fe_snmp_scan = lambda oid: "FireEye" in oid(".1.3.6.1.2.1.1.1.0")

fe_snmp_info = {
                 'sysinfo':  (".1.3.6.1.4.1.25597.11.1.1", [ 1, 2, 3 ]),
                 'sysimage': (".1.3.6.1.4.1.25597.11.5.1", [ 1, 2, 3, 4 ]),
                 'scontent': (".1.3.6.1.4.1.25597.11.5.1", [ 5, 6, 7 ]),
               }

def inventory_fe_generic(info):
    if info:
        return [(None, None)]

def check_fe_sysinfo(_item, _params, info):
    if info:
        status, model, serial = info[0]

        return 0, "HW-Model %s, SNR %s, Status is \"%s\"" % (model, serial, status)
    else:
        return 3, "SysInfo not found in SNMP data"

def check_fe_sysimage(_item, _params, info):
    if info:
        name, version_current, version_latest, is_latest = info[0]

        return 0, "Image %s, Version (installed/available) %s/%s is latest: %s" % (name, version_current, version_latest, fe_truefalse[is_latest])
    else:
        return 3, "SysImage info not found in SNMP data"

def check_fe_seccontent(_item, _params, info):
    if info:
        version, upd_passed, upd_time = info[0]

        return 0, "SecurityContent Version %s, last update %s at %s" % (version, fe_update[upd_passed], upd_time)
    else:
        return 3, "SecurityContent info not found in SNMP data"

check_info['fireeye.sysinfo'] = {
    "check_function"      : check_fe_sysinfo,
    "inventory_function"  : inventory_fe_generic,
    "has_perfdata"        : False,
    "service_description" : "FE SysInfo",
    "snmp_scan_function"  : fe_snmp_scan,
    "snmp_info"           : fe_snmp_info['sysinfo'],
}

check_info['fireeye.sysimage'] = {
    "check_function"      : check_fe_sysimage,
    "inventory_function"  : inventory_fe_generic,
    "has_perfdata"        : False,
    "service_description" : "FE SysImage",
    "snmp_scan_function"  : fe_snmp_scan,
    "snmp_info"           : fe_snmp_info['sysimage'],
}

check_info['fireeye.seccontent'] = {
    "check_function"      : check_fe_seccontent,
    "inventory_function"  : inventory_fe_generic,
    "has_perfdata"        : False,
    "service_description" : "FE SecContent",
    "snmp_scan_function"  : fe_snmp_scan,
    "snmp_info"           : fe_snmp_info['scontent'],
}
