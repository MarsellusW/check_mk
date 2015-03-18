#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def check_fireeye_temp(_item, _params, info):
    if info:
        status, healthy, temp = info[0]

        rc = 0

        label = ''
        msgtxt = 'healthy'
        healthy = fireeye_truefalse[healthy]
        temp = int(temp)

        perfdata = [("temp", temp)]

        if not healthy:
            rc = 1
            label = '(!)'
            msgtxt = 'un%s' % msgtxt

        return rc, "Temperature is %s (\"%s\")%s, currently %d°C" % (msgtxt, status, label, temp), perfdata
    else:
        return 3, "TemperatureInfo not found in SNMP data"

check_info["fireeye_temp"] = {
    "check_function"      : check_fireeye_temp,
    "inventory_function"  : inventory_fireeye_generic,
    "has_perfdata"        : True,
    "service_description" : "FE Temperature",
#    "group"               : "room_temperature",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.1.1", [ 5, 6, 4 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include" ],
}
