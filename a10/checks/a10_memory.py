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
        # SNMP data is in kBytes, so let's get Bytes out of it
        total = int(info[0][0]) * 1024
        used  = int(info[0][1]) * 1024

        warn, crit = params['levels']

        warn = total * warn / 100
        crit = total * crit / 100

        state = 0
        label = ""

        perfdata = [("used", used, warn, crit, total)]

        if used >= crit:
            state = 2
            label = "(!!)"
        elif used >= warn:
            state = 1
            label = "(!)"

        infotext = "%s%s of %s used" % (get_bytes_human_readable(used), label,
                                        get_bytes_human_readable(total))
        infotext += " (levels at %s/%s)" % (get_bytes_human_readable(warn),
                                            get_bytes_human_readable(crit))

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
