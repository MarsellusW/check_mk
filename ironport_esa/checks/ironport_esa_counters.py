#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import pprint

state_label = {
    0: '',
    1: '(!)',
    2: '(!!)',
    3: '(!!!)',
}

ironport_esa_counter_names = {
    'hard_bounced_recips': 'Total',
    '5xx_hard_bounced_recips': '5XX',
    'dns_hard_bounced_recips': 'DNS',
    'expired_hard_bounced_recips': 'Expired',
    'filter_hard_bounced_recips': 'Filter',
    'other_hard_bounced_recips': 'Other',
    'completed_recips': 'Total',
    'deleted_recips': 'Deleted',
    'global_unsub_hits': 'Global Unsub Hits',
    'delivered_recips': 'Delivered',
    'inj_msgs': 'Messages Received',
    'inj_recips': 'Recipients Received',
    'gen_bounce_recips': 'Generated Bounce Recipients',
    'rejected_recips': 'Rejected Recipients',
    'dropped_msgs': 'Dropped Messages',
    'soft_bounced_evts': 'Soft Bounce Events',
    'dns_reqs': 'DNS Requests',
    'network_reqs': 'Network Requests',
    'cache_hits': 'Cache Hits',
    'cache_misses': 'Cache Misses',
    'cache_exceptions': 'Cache Exceptions',
    'cache_expired': 'Cache Expired',
}

ironport_esa_counter_types = {
    'bounces': [
        'hard_bounced_recips',
        '5xx_hard_bounced_recips',
        'dns_hard_bounced_recips',
        'expired_hard_bounced_recips',
        'filter_hard_bounced_recips',
        'other_hard_bounced_recips',
    ],
    'completions': [
        'completed_recips',
        'deleted_recips',
        'global_unsub_hits',
        'delivered_recips',
    ],
    'mailhandling': [
        'inj_msgs',
        'inj_recips',
        'gen_bounce_recips',
        'rejected_recips',
        'dropped_msgs',
        'soft_bounced_evts',
    ],
    'dnsstatus': [
        'dns_reqs',
        'network_reqs',
        'cache_hits',
        'cache_misses',
        'cache_exceptions',
        'cache_expired',
    ],
}


def inventory_ironport_esa_counters(info, checktype):
    cntrs = [l[0] for l in info]

    # inventory if first defined counter for checktype matches
    if ironport_esa_counter_types[checktype][0] in cntrs:
        return [(None, None)]

    return []


def check_ironport_esa_counters(info, checktype):
    this_time = time.time()  # pylint: disable=E0602
    values = {}
    msgs = []
    perfdata = []

    cntrs = ironport_esa_counter_types[checktype]

    wrapped = False

    # pylint: disable=E0602
    for cntr, value in info:
        if cntr in cntrs:
            try:
                _timedif, rate = get_counter(
                    "counters.%s.%s" %
                    (checktype, cntr), this_time, saveint(value))
                values[cntr] = rate
            except MKCounterWrapped:
                wrapped = True

    if wrapped:
        raise MKCounterWrapped("Counter wrap")
    # pylint: enable=E0602

    for cntr in cntrs:
        name = ironport_esa_counter_names[cntr]
        value = savefloat(values[cntr])  # pylint: disable=E0602
        msgs.append("%s: %.3f/s" % (name, value))
        perfdata.append(('"%s"' % name, value))

    if msgs:
        return (0, ', '.join(msgs), perfdata)
    else:
        return (3, 'No data received')


def check_ironport_esa_bounces(_no_item, _no_params, info):
    return check_ironport_esa_counters(info, 'bounces')


# pylint: disable=E0602
check_info['ironport_esa_counters.bounces'] = {
    "check_function": check_ironport_esa_bounces,
    "inventory_function": lambda info:
        inventory_ironport_esa_counters(info, 'bounces'),
    "has_perfdata": True,
    "service_description": "IronPort Hard Bounced Recipients",
}
# pylint: enable=E0602


def check_ironport_esa_completions(_no_item, _no_params, info):
    return check_ironport_esa_counters(info, 'completions')


# pylint: disable=E0602
check_info['ironport_esa_counters.completions'] = {
    "check_function": check_ironport_esa_completions,
    "inventory_function": lambda info:
        inventory_ironport_esa_counters(info, 'completions'),
    "has_perfdata": True,
    "service_description": "IronPort Completed Recipients",
}
# pylint: enable=E0602


def check_ironport_esa_mailhandling(_no_item, _no_params, info):
    return check_ironport_esa_counters(info, 'mailhandling')


# pylint: disable=E0602
check_info['ironport_esa_counters.mailhandling'] = {
    "check_function": check_ironport_esa_mailhandling,
    "inventory_function": lambda info:
        inventory_ironport_esa_counters(info, 'mailhandling'),
    "has_perfdata": True,
    "service_description": "IronPort Mail Handling Events",
}
# pylint: enable=E0602


def check_ironport_esa_dnsstatus(_no_item, _no_params, info):
    return check_ironport_esa_counters(info, 'dnsstatus')


# pylint: disable=E0602
check_info['ironport_esa_counters.dnsstatus'] = {
    "check_function": check_ironport_esa_dnsstatus,
    "inventory_function": lambda info:
        inventory_ironport_esa_counters(info, 'dnsstatus'),
    "has_perfdata": True,
    "service_description": "IronPort DNS Status",
}
# pylint: enable=E0602
