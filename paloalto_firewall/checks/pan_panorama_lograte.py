#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

paloalto_lograte_default_levels = (0, 0)


def inventory_paloalto_lograte(info):
    if info:
        return [(None, "paloalto_lograte_default_levels")]


def check_paloalto_lograte(_item, params, info):
    if info:
        rate = int(info[0][0])

        warn, crit = params
        if int(warn) == 0:
            warn = None
        if int(crit) == 0:
            crit = None

        state = 0
        label = ""

        perfdata = [("rate", rate, warn, crit)]

        if crit > 0 and rate <= crit:
            state = 2
            label = "(!!)"
        elif warn > 0 and rate <= warn:
            state = 1
            label = "(!)"

        return (state, "currently writing %d LOGS/s" % rate, perfdata)
    else:
        return (3, "No data retrieved")

check_info['pan-panorama_lograte'] = {
    "check_function": check_paloalto_lograte,
    "inventory_function": inventory_paloalto_lograte,
    "has_perfdata": True,
    "service_description": "Panorama Log Rate",
    #    "group"               : "room_temperature",
    "snmp_scan_function": lambda oid: oid(".1.3.6.1.2.1.1.2.0") in [
        ".1.3.6.1.4.1.25461.2.3.16",
        ".1.3.6.1.4.1.25461.2.3.30"],
    "snmp_info": (
        ".1.3.6.1.4.1.25461.2.3.16.1", ["1.0",  # LOG writes/s panLcLogRate
                                        ]
    ),
}
