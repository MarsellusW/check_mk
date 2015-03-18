#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

factory_settings["memory_default_levels"] = {
    "levels" : (80.0, 90.0),
}

def inventory_a10_memory(info):
    if info:
        return [ (None, "memory_default_levels") ]

def check_a10_memory(item, params, info):
    if info:
        # SNMP data is in kBytes, so let's get MBytes out of it
        total_mb = saveint(info[0][0]) / 1024.0
        used_mb  = saveint(info[0][1]) / 1024.0

        try:
            warn, crit = params['levels']
        except:
            warn, crit = params

        warn = total_mb * warn / 100
        crit = total_mb * crit / 100

        state = 0
        label = ""

        perfdata = [("used", used_mb, warn, crit, 0, total_mb)]

        if used_mb >= crit:
            state = 2
            label = "(!!)"
        elif used_mb >= warn:
            state = 1
            label = "(!)"

        infotext = "%.1fMB%s of %.1fMB used" % (used_mb, label, total_mb)
        infotext += " (levels at %.1f/%.1f)" % (warn, crit)

        return (state, infotext, perfdata)

    return (3, "No data received for %s" % item)

check_info['a10_memory'] = {
    "check_function"          : check_a10_memory,
    "inventory_function"      : inventory_a10_memory,
    "has_perfdata"            : True,
    "service_description"     : "Memory used",
    "group"                   : "memory",
    "default_levels_variable" : "memory_default_levels",
    "snmp_scan_function"      : lambda oid: "AX Series" in oid(".1.3.6.1.2.1.1.1.0"),
    "snmp_info"               : ('.1.3.6.1.4.1.22610.2.4.1.2', [
                                       '1', # total 
                                       '2'  # usage
                                     ]),
}
