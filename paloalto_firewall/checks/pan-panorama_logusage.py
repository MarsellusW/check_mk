#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

paloalto_logusage_default_levels = (0, 0)

def inventory_paloalto_logusage(info):
    if info:
        return [ (None, "paloalto_logusage_default_levels") ]

def check_paloalto_logusage(_item, params, info):
    if info:
        warn, crit = params
        if int(warn) == 0: warn = None
        if int(crit) == 0: crit = None

        usages = [
                  ('Ld1', int(info[0][0]), warn, crit),
                  ('Ld2', int(info[0][1]), warn, crit),
                  ('Ld3', int(info[0][2]), warn, crit),
                  ('Ld4', int(info[0][3]), warn, crit)
                  ]

        state = 0
        txtmsg = []

        perfdata = [ (x[0], x[1], warn, crit) for x in usages ]

        for ld in usages:
            label = ""
            name, usage, warn, crit = ld

            if crit > 0 and usage <= crit:
                state = max(state, 2)
                label = "(!!)"
            elif warn > 0 and usage <= warn:
                state = max(state, 1)
                label = "(!)"

            txtmsg.append("%s: %d%s " % (name, usage, label))

        return (state, ', '.join(txtmsg), perfdata)
    else:
        return (3, "No data retrieved")

check_info['pan-panorama_logusage'] = {
    "check_function"      : check_paloalto_logusage,
    "inventory_function"  : inventory_paloalto_logusage,
    "has_perfdata"        : True,
    "service_description" : "Panorama Log Usage %s",
#    "group"               : "room_temperature",
    "snmp_scan_function"  : lambda oid: oid(".1.3.6.1.2.1.1.2.0") in [".1.3.6.1.4.1.25461.2.3.16", ".1.3.6.1.4.1.25461.2.3.30"],
    "snmp_info"           : (
       ".1.3.6.1.4.1.25461.2.3.16.1.3", [ "1.0",  # LOG usage panLcDiskUsageLd1
                                          "2.0",  # LOG usage panLcDiskUsageLd2
                                          "3.0",  # LOG usage panLcDiskUsageLd3
                                          "4.0",  # LOG usage panLcDiskUsageLd4
                                     ]
   ),
}
