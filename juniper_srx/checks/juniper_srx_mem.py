#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK check providing a Service for memory utilization of Juniper SRX.
"""

import re

factory_settings['srx_mem_re_default_levels'] = {  # pylint: disable=E0602
    'levels': (80.0, 95.0),
}

label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}

srx_mem_snmp_info = [
    ['.1.3.6.1.4.1.2636.3.1.13.1', [
        5,  # jnxOperatingDescr
        18,  # jnxOperatingChassisDescr
        15,  # jnxOperatingMemory
        11,  # jnxOperatingBuffer
    ]],
    ['.1.3.6.1.4.1.2636.3.39.1.12.1.1.1', [
        11,  # jnxJsSPUMonitoringNodeDescr
        2,  # jnxJsSPUMonitoringFPCIndex
        3,  # jnxJsSPUMonitoringSPUIndex
        5,  # jnxJsSPUMonitoringMemoryUsage
    ]],
    ['.1.3.6.1.2.1.1', ['2.0']]
]

srx_branch_mem_breakdown = {
    512.0: {
        'Control plane': 336.0,
        'Data plane': 176.0,
    },
    1024.0: {
        'Control plane': 560.0,
        'Data plane': 464.0,
    },
    2048.0: {
        'Control plane': 1104.0,
        'Data plane': 944.0,
    },
}


def inventory_srx_mem_re(info):
    """Return memory inventory data for each routing engine."""
    inventory = []

    if info[0] is not None:
        for line in info[0]:
            if "Routing Engine" in line[0] and line[2] != '0':
                inventory.append((line[0], "srx_mem_re_default_levels"))

    return inventory


def check_srx_mem_re(item, params, info):
    """Return memory data for the requested routing engine."""
    for line in info[0]:
        if line[0] != item:
            continue

        mem = {}
        total = float(line[2])
        util = float(line[3])

        if info[2][0][0] in srx_model_branch:  # pylint: disable=E0602
            chassis = line[1]

            for pfe in info[1]:
                if re.match(pfe[0], chassis, flags=re.IGNORECASE):
                    mem['pfe'] = float(pfe[3])
                    break

            mem['cplane'] = srx_branch_mem_breakdown[total]['Control plane']
            mem['dplane'] = srx_branch_mem_breakdown[total]['Data plane']

            util = (
                (util * total) - (mem['pfe'] * mem['dplane'])) / mem['cplane']

        warn, crit = params['levels']

        perfdata = [("util", util, warn, crit, 0, 100), ("total", total)]

        state = 2 if util >= crit else 1 if util >= warn else 0

        return (state, "%.1f%%%s used" % (util, label[state]), perfdata)

    return (3, "No data received for %s" % item)


# pylint: disable=E0602
check_info['juniper_srx_mem.re'] = {
    "check_function": check_srx_mem_re,
    "inventory_function": inventory_srx_mem_re,
    "has_perfdata": True,
    "service_description": "Memory used %s",
    "group": 'memory',
    "default_levels_variable": "srx_mem_re_default_levels",
    "snmp_scan_function": srx_snmp_scan,
    "snmp_info": srx_mem_snmp_info,
    "includes": ["juniper_srx.include"],
}
# pylint: enable=E0602


def inventory_srx_mem_pfe(info):
    """Return memory inventory data for each package forwarding engine."""
    inventory = []

    if info[1]:
        for line in info[1]:
            name = "%s FPC %s/SPU %s" % (line[0], line[1], line[2])
            inventory.append((name, "srx_mem_re_default_levels"))

    return inventory


def check_srx_mem_pfe(item, params, info):
    """Return memory data for the requested package forwarding engine."""
    info = info[1]

    for line in info:
        name = "%s FPC %s/SPU %s" % (line[0], line[1], line[2])

        if name != item:
            continue

        util = int(line[3])

        warn, crit = params['levels']

        perfdata = [("util", util, warn, crit, 0, 100)]

        state = 2 if util >= crit else 1 if util >= warn else 0

        return (
            state, "%d%%%s used" % (util, label[state]), perfdata)

    return (3, "No data received for %s" % item)


# pylint: disable=E0602
check_info['juniper_srx_mem.pfe'] = {
    "check_function": check_srx_mem_pfe,
    "inventory_function": inventory_srx_mem_pfe,
    "has_perfdata": True,
    "service_description": "Memory used %s",
    "group": 'memory',
    "default_levels_variable": "srx_mem_re_default_levels",
    "snmp_scan_function": srx_snmp_scan,
    "snmp_info": srx_mem_snmp_info, "includes": ["juniper_srx.include"],
}
# pylint: enable=E0602
