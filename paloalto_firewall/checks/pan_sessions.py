#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

paloalto_sessions_default_levels = (80, 90)

def inventory_paloalto_sessions(info):
    if len(info[0]) >= 5:
        return [ (None, "paloalto_sessions_default_levels") ]

def check_paloalto_sessions(_item, params, info):
    if len(info[0]) >= 5:
        s_util, s_max, s_act, s_tcp, s_udp, s_icmp, s_ssl, s_ssl_util = map(int, info[0])

        warn, crit = params

        state = 0
        label = ""

        perfdata = [
                    ("util", s_util, warn, crit),
                    ("max" , s_max),
                    ("total" , s_act),
                    ("tcp" , s_tcp),
                    ("udp" , s_udp),
                    ("icmp", s_icmp),
                    ("ssl", s_ssl) ]

        if s_util >= crit:
            state = 2
            label = "(!!)"
        elif s_util >= warn:
            state = 1
            label = "(!)"

        return (state, "%d active sessions (%d TCP, %d UDP, %d ICMP, %d SSL proxy), %d%%%s of %d maximum sessions used" % (s_act, s_tcp, s_udp, s_icmp, s_ssl, s_util, label, s_max), perfdata)
    else:
        return (3, "No data retrieved")

check_info['pan-sessions'] = {
    "check_function"      : check_paloalto_sessions,
    "inventory_function"  : inventory_paloalto_sessions,
    "has_perfdata"        : True,
    "service_description" : "Sessions",
#    "group"               : "room_temperature",
    "snmp_scan_function"  : lambda oid: "Palo Alto Networks" in oid(".1.3.6.1.2.1.1.1.0"),
    "snmp_info"           : (
       ".1.3.6.1.4.1.25461.2.1.2.3", [ "1.0",  # % session utilization
                                       "2.0",  # Max Sessions for the device
                                       "3.0",  # Total Active Sessions
                                       "4.0",  # Active TCP Sessions
                                       "5.0",  # Active UDP Sessions
                                       "6.0",  # Active ICMP Sessions
                                       "7.0",  # Active SSL proxy Sessions
                                       "8.0"  # % SSL proxy session utilization
                                     ]
   ),
}
