#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

google_gsa_status = {
                     0: ("green", ""),
                     1: ("yellow", "(!)"),
                     2: ("red", "(!!)")
                    }

gsa_snmp_scan = lambda oid: "GSA Version" in oid(".1.3.6.1.2.1.1.1.0")

gsa_snmp_info = {
                 'disk': ( ".1.3.6.1.4.1.11129.1.3.1", [
                             1,
                             2,
                             ]
                         ),
                 'temp': ( ".1.3.6.1.4.1.11129.1.3.2", [
                             1,
                             2,
                             ]
                         ),
                 'syst': ( ".1.3.6.1.4.1.11129.1.3.3", [
                             1,
                             2,
                             ]
                         ),
                }

def inventory_google_gsa_health(info):
    if info:
        return [(None, None)]

def check_google_gsa_health(_item, _params, info):
    if info:
        status, errtxt = info[0]

        if errtxt:
            errtxt = ", reported error is \"%s\"" % errtxt

        txt, label = google_gsa_status[int(status)]

        return int(status), "health status is \"%s\"%s%s" % (txt, label, errtxt)
    else:
        return 3, "Item not found in SNMP data"

check_info['google_gsa_health.disk'] = {
    "check_function"      : check_google_gsa_health,
    "inventory_function"  : inventory_google_gsa_health,
    "has_perfdata"        : False,
    "service_description" : "GSA disk",
    "snmp_scan_function"  : gsa_snmp_scan,
    "snmp_info"           : gsa_snmp_info['disk'],
}

check_info['google_gsa_health.temp'] = {
    "check_function"      : check_google_gsa_health,
    "inventory_function"  : inventory_google_gsa_health,
    "has_perfdata"        : False,
    "service_description" : "GSA temperature",
    "snmp_scan_function"  : gsa_snmp_scan,
    "snmp_info"           : gsa_snmp_info['temp'],
}

check_info['google_gsa_health.system'] = {
    "check_function"      : check_google_gsa_health,
    "inventory_function"  : inventory_google_gsa_health,
    "has_perfdata"        : False,
    "service_description" : "GSA system",
    "snmp_scan_function"  : gsa_snmp_scan,
    "snmp_info"           : gsa_snmp_info['syst'],
}
