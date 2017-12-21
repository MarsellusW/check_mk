#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

import pprint

state_label = {
    0: '',
    1: '(!)',
    2: '(!!)',
    3: '(!!!)',
}

calc_unit = {
    'k': 1000,
    'M': 1000 * 1000,
    'G': 1000 * 1000 * 1000,
}

factory_settings['ironport_esa_cpu_default_levels'] = {  # pylint: disable=E0602
    'cpu': (90.0, 95.0),
}

ironport_esa_gauge_names = {
    'active_recips': 'Total Active',
    'attempted_recips': 'Attempted',
    'av_utilization': 'Anti-Virus',
    'bm_utilization': 'BrightMail',
    'case_utilization': 'Anti-Spam',
    'conn_in': 'Connections In',
    'conn_out': 'Connections Out',
    'cpu_utilization': 'Appliance',
    'dests_in_memory': 'Destination Objects in Memory',
    'disk_utilization': 'Disk utilization',
    'kbytes_free': 'Total Free',
    'kbytes_in_quarantine': 'Used by Quarantine',
    'kbytes_used': 'Total Used',
    'log_available': 'Available',
    'log_used': 'Utilization',
    'msgs_in_quarantine': 'Messages in Quarantine',
    'msgs_in_work_queue': 'Messages in Work queue',
    'quarantine_utilization': 'Quarantine',
    'ram_utilization': 'Memory utilization',
    'reporting_utilization': 'Reporting',
    'resource_conservation': 'Resource conservation',
    'total_utilization': 'Total',
    'unattempted_recips': 'Unattempted',
}

ironport_esa_gauge_types = {
    'cpu': [
        'total_utilization',
        'cpu_utilization',
        'case_utilization',
        # 'bm_utilization',  # BrightMail, an older Anti-Spam engine
        'av_utilization',
        'reporting_utilization',
        'quarantine_utilization',
    ],
    'mailprocessing': [
        'conn_in',
        'conn_out',
        'dests_in_memory',
        'msgs_in_quarantine',
        'msgs_in_work_queue',
    ],
    'activerecips': [
        'active_recips',
        'attempted_recips',
        'unattempted_recips'
    ],
    'queuespace': [
        'kbytes_free',
        'kbytes_in_quarantine',
        'kbytes_used',
    ],
    'genutil': [
        'disk_utilization',
        'ram_utilization',
        'resource_conservation',
    ],
    'logdisk': [
        'log_available',
        'log_used',
    ],
}

ironport_esa_gauge_mapping = {  # diffs between fw-version 7.6.1 and 9.1.0
    'msgs_in_policy_virus_outbreak_quarantine': 'msgs_in_quarantine',
    'kbytes_in_policy_virus_outbreak_quarantine': 'kbytes_in_quarantine',
}


def inventory_ironport_esa_gauges(info, checktype):
    gauges = [l[0] for l in info]

    # inventory if first defined gauge for checktype matches
    if ironport_esa_gauge_types[checktype][0] in gauges:
        if checktype == "cpu":
            return [(None, "ironport_esa_cpu_default_levels")]
        else:
            return [(None, None)]

    return []


def check_ironport_esa_gauges(params, info, checktype):
    values = {}
    msgs = []
    perfdata = []
    state_all = 0

    gauges = ironport_esa_gauge_types[checktype]

    for gauge, value in info:
        if gauge == 'log_available':
            value, unit = (value[:3], value[-1:])
            value = int(value) * calc_unit[unit]

        if gauge in ironport_esa_gauge_mapping:
            gauge = ironport_esa_gauge_mapping[gauge]

        values[gauge] = saveint(value)  # pylint: disable=E0602

    for gauge in gauges:
        levels = ""
        state = 0
        warn = crit = None
        name = ironport_esa_gauge_names[gauge]
        value = saveint(values[gauge])  # pylint: disable=E0602

        if checktype == 'cpu' and name == "Total":
            warn, crit = params['cpu']
            state = 2 if value >= crit else 1 if value >= warn else 0

            if state > 0:
                state_all = max(state_all, state)
                levels = " (levels at %.1f/%.1f)" % (warn, crit)

        perfdata.append(('"%s"' % name, value, warn, crit))

        if gauge == 'log_available':
            value = value / calc_unit[unit]
            unit = " " + unit + "B"
        else:
            unit = ""

        msgs.append(
            "%s: %d%s%s%s" %
            (name, value, unit, state_label[state], levels))

    if msgs:
        return (state_all, ', '.join(msgs), perfdata)
    else:
        return (3, 'No data received')


def check_ironport_esa_cpu(_no_item, params, info):
    return check_ironport_esa_gauges(params, info, 'cpu')


# pylint: disable=E0602
check_info['ironport_esa_gauges.cpu'] = {
    "check_function": check_ironport_esa_cpu,
    "inventory_function": lambda info:
        inventory_ironport_esa_gauges(info, 'cpu'),
    "group": 'cpu_utilization',
    "default_levels_variable": "ironport_esa_cpu_default_levels",
    "has_perfdata": True,
    "service_description": "CPU utilization",
}
# pylint: enable=E0602


def check_ironport_esa_mailprocessing(_no_item, params, info):
    return check_ironport_esa_gauges(params, info, 'mailprocessing')


# pylint: disable=E0602
check_info['ironport_esa_gauges.mailprocessing'] = {
    "check_function": check_ironport_esa_mailprocessing,
    "inventory_function": lambda info:
        inventory_ironport_esa_gauges(info, 'mailprocessing'),
    "has_perfdata": True,
    "service_description": "IronPort Mail Processing",
}
# pylint: enable=E0602


def check_ironport_esa_activerecips(_no_item, params, info):
    return check_ironport_esa_gauges(params, info, 'activerecips')


# pylint: disable=E0602
check_info['ironport_esa_gauges.activerecips'] = {
    "check_function": check_ironport_esa_activerecips,
    "inventory_function": lambda info:
        inventory_ironport_esa_gauges(info, 'activerecips'),
    "has_perfdata": True,
    "service_description": "IronPort Active Recipients",
}
# pylint: enable=E0602


def check_ironport_esa_queuespace(_no_item, params, info):
    return check_ironport_esa_gauges(params, info, 'queuespace')


# pylint: disable=E0602
check_info['ironport_esa_gauges.queuespace'] = {
    "check_function": check_ironport_esa_queuespace,
    "inventory_function": lambda info:
        inventory_ironport_esa_gauges(info, 'queuespace'),
    "has_perfdata": True,
    "service_description": "IronPort Queue Space",
}
# pylint: enable=E0602


def check_ironport_esa_genutil(_no_item, params, info):
    return check_ironport_esa_gauges(params, info, 'genutil')


# pylint: disable=E0602
check_info['ironport_esa_gauges.genutil'] = {
    "check_function": check_ironport_esa_genutil,
    "inventory_function": lambda info:
        inventory_ironport_esa_gauges(info, 'genutil'),
    "has_perfdata": True,
    "service_description": "IronPort General Utilization",
}
# pylint: enable=E0602


def check_ironport_esa_logdisk(_no_item, params, info):
    return check_ironport_esa_gauges(params, info, 'logdisk')


# pylint: disable=E0602
check_info['ironport_esa_gauges.logdisk'] = {
    "check_function": check_ironport_esa_logdisk,
    "inventory_function": lambda info:
        inventory_ironport_esa_gauges(info, 'logdisk'),
    "has_perfdata": True,
    "service_description": "IronPort Logging Disk Utilization",
}
# pylint: enable=E0602
