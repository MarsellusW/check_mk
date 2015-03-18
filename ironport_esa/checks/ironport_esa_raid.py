#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK service showing the RAID status of an IronPort Appliance.
"""


def inventory_iport_dnsunfinished(info):
    if info:
        return [(None, None)]
    else:
        return []


def check_iport_dnsunfinished(_no_item, _no_params, info):
    if info:
        outstanding, pending = info[0]

        msg = "outstanding: %s, pending: %s" % (outstanding, pending)

        perfdata = [("outstanding", outstanding), ("pending", pending)]

        return(0, msg, perfdata)
    return(3, "no data found")


# pylint: disable=E0602
check_info['ironport_esa_dnsunfinished'] = {
    "check_function": check_iport_dnsunfinished,
    "inventory_function": inventory_iport_dnsunfinished,
    "has_perfdata": True,
    "service_description": "IronPort unfinished DNS requests",
    "snmp_scan_function": ironport_snmp_scan,
    "snmp_info": (".1.3.6.1.4.1.15497.1.1.1", [
        15,  # outstandingDNSRequests
        16  # pendingDNSRequests
    ]),
    "includes": ["ironport.include"],
}
# pylint: enable=E0602
