#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK service showing the number of messages in Work Queue.
"""


def inventory_iport_workqueue(info):
    if info:
        return [(None, None)]
    else:
        return []


def check_iport_workqueue(_no_item, _no_params, info):
    if info:
        messages = info[0][0]

        msg = "Messages in Queue: %s" % messages

        perfdata = [("messages", messages)]

        return(0, msg, perfdata)
    return(3, "no data found")


# pylint: disable=E0602
check_info['ironport_esa_workqueue'] = {
    "check_function": check_iport_workqueue,
    "inventory_function": inventory_iport_workqueue,
    "has_perfdata": True,
    "service_description": "IronPort Work Queue",
    "snmp_scan_function": ironport_snmp_scan,
    "snmp_info": (".1.3.6.1.4.1.15497.1.1.1", [
        11  # workQueueMessages
    ]),
    "includes": ["ironport.include"],
}
# pylint: enable=E0602
