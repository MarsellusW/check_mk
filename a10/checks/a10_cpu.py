#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

factory_settings["a10_cpu_default_levels"] = {'cpu': (80.0, 90.0),}

a10_cpus = {
            0: "average",
            1: "Control",
            2: "Data"
            }

def inventory_a10_cpu(info):
    if info:
        return [ (None, "a10_cpu_default_levels") ]

def check_a10_cpu(item, params, info):
    if info:
        warn, crit = params['cpu']
        state      = 0
        infotxt    = []
        perfdata   = []

        for cpu in a10_cpus:
            if info[0][cpu]:
                name  = a10_cpus[cpu]
                util  = saveint(info[0][cpu])
                label = ""

                perfdata.append(('"%s"' % name, util, warn, crit, 0, 100))

                if util >= crit:
                    state = max(2, state)
                    label = "(!!)"
                elif util >= warn:
                    state = max(1, state)
                    label = "(!)"

                infotxt.append("%s CPU %d%%%s" %(name, util, label))

        return (state, ", ".join(infotxt) + " (levels at %.1f/%.1f)" % (warn, crit), perfdata)

    return (3, "No data received for %s" % item)

check_info['a10_cpu'] = {
    "check_function"          : check_a10_cpu,
    "inventory_function"      : inventory_a10_cpu,
    "has_perfdata"            : True,
    "service_description"     : "CPU utilization",
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
