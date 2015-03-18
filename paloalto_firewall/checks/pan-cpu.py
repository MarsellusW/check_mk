#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

paloalto_cpu_default_levels = (80.0, 90.0)

pan_cpus = {
            1: "MgmtPlane",
            2: "DataPlane-System",
            3: "DataPlane-Packets"
            }

def inventory_paloalto_cpu(info):
    if info:
        return [ (pan_cpus[x + 1], "paloalto_cpu_default_levels") for x in range(len(info[0])) if info[0][x] ]

def check_paloalto_cpu(item, params, info):
    if info:
        for x in range(len(info[0])):
            if info[0][x] and pan_cpus[x + 1] == item:
                util = int(info[0][x])

                warn, crit = params

                state = 0
                label = ""

                perfdata = [("util", util, warn, crit, 0, 100)]

                if util >= crit:
                    state = 2
                    label = "(!!)"
                elif util >= warn:
                    state = 1
                    label = "(!)"

                return (state, "%d%% utilization" % util, perfdata)

    return (3, "No data retceived for %s" % item)

check_info['pan-cpu'] = {
    "check_function"      : check_paloalto_cpu,
    "inventory_function"  : inventory_paloalto_cpu,
    "has_perfdata"        : True,
    "service_description" : "CPU utilization %s",
    "group"               : 'cpu_utilization',
    "snmp_scan_function"  : lambda oid: "Palo Alto Networks" in oid(".1.3.6.1.2.1.1.1.0"),
    "snmp_info"           : ('.1.3.6.1.2.1.25.3.3.1.2', ['1', '2', '3']),
}
