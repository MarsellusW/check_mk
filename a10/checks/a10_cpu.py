#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

factory_settings['a10_cpu_default_levels'] = {'cpu': (80.0, 90.0),}

a10_cpus = {
            1: "overall",
            2: "Control CPU",
            3: "Data CPU"
            }

def inventory_a10_cpu(info):
    if info:
        return [ (a10_cpus[x + 1], "a10_cpu_default_levels") for x in range(len(info[0])) if info[0][x] ]

def check_a10_cpu(item, params, info):
    if info:
        for x in range(len(info[0])):
            if info[0][x] and a10_cpus[x + 1] == item:
                util = int(info[0][x])

                warn, crit = params['cpu']

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

    return (3, "No data received for %s" % item)

check_info['a10_cpu'] = {
    "check_function"          : check_a10_cpu,
    "inventory_function"      : inventory_a10_cpu,
    "has_perfdata"            : True,
    "service_description"     : "CPU utilization %s",
    "group"                   : 'cpu_utilization',
    "default_levels_variable" : "a10_cpu_default_levels",
    "snmp_scan_function"      : lambda oid: "AX Series" in oid(".1.3.6.1.2.1.1.1.0"),
    "snmp_info"               : ('.1.3.6.1.4.1.22610.2.4.1.3', 
                                     [
                                       '3', # A10AvgCpuUsage
                                       '4', # A10CtrlCpuUsage
                                       '5'  # A10DataCpuUsage
                                     ]),
}
