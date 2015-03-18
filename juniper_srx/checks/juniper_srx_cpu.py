#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK check providing a Service for CPU utilization of Juniper SRX.
"""

factory_settings['srx_cpu_re_default_levels'] = {  # pylint: disable=E0602
    'cpu': (85.0, 95.0),
}

label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}

srx_cpu_snmp_info = [
    ['.1.3.6.1.4.1.2636.3.1.13.1', [
        5,  # jnxOperatingDescr
        8,  # jnxOperatingCPU
    ]],
    ['.1.3.6.1.4.1.2636.3.39.1.12.1.1.1', [
        11,  # jnxJsSPUMonitoringNodeDescr
        2,  # jnxJsSPUMonitoringFPCIndex
        3,  # jnxJsSPUMonitoringSPUIndex
        4,  # jnxJsSPUMonitoringCPUUsage
    ]]
]


def inventory_srx_cpu_re(info):
    """Return CPU inventory data for each routing engine."""
    inventory = []

    if info[0] is not None:
        for line in info[0]:
            if "Routing Engine" in line[0]:
                inventory.append((line[0], "srx_cpu_re_default_levels"))

    return inventory


def check_srx_cpu_re(item, params, info):
    """Return CPU data for the requested routing engine."""
    info = info[0]

    for line in info:
        if line[0] == item:
            util = int(line[1])

            warn, crit = params['cpu']

            perfdata = [("util", util, warn, crit, 0, 100)]

            state = 2 if util >= crit else 1 if util >= warn else 0

            return (state, "%d%%%s utilized" % (util, label[state]), perfdata)

    return (3, "No data received for %s" % item)


# pylint: disable=E0602
check_info['juniper_srx_cpu.re'] = {
    "check_function": check_srx_cpu_re,
    "inventory_function": inventory_srx_cpu_re,
    "has_perfdata": True,
    "service_description": "CPU utilization %s",
    "group": 'cpu_utilization',
    "default_levels_variable": "srx_cpu_re_default_levels",
    "snmp_scan_function": srx_snmp_scan,
    "snmp_info": srx_cpu_snmp_info,
    "includes": ["juniper_srx.include"],
}
# pylint: enable=E0602


def inventory_srx_cpu_pfe(info):
    """Return CPU inventory data for each package forwarding engine."""
    inventory = []

    if info[1] is not None:
        for line in info[1]:
            name = "%s FPC %s/SPU %s" % (line[0], line[1], line[2])
            inventory.append((name, "srx_cpu_re_default_levels"))

    return inventory


def check_srx_cpu_pfe(item, params, info):
    """Return CPU data for the requested package forwarding engine."""
    info = info[1]

    for line in info:
        node, fpc, spu = line[0:3]
        name = "%s FPC %s/SPU %s" % (node, fpc, spu)

        if name == item:
            util = int(line[3])

            warn, crit = params['cpu']

            perfdata = [("util", util, warn, crit, 0, 100)]

            state = 2 if util >= crit else 1 if util >= warn else 0

            return (state, "%d%%%s utilized" % (util, label[state]), perfdata)

    return (3, "No data received for %s" % item)


# pylint: disable=E0602
check_info['juniper_srx_cpu.pfe'] = {
    "check_function": check_srx_cpu_pfe,
    "inventory_function": inventory_srx_cpu_pfe,
    "has_perfdata": True,
    "service_description": "CPU utilization %s",
    "group": 'cpu_utilization',
    "default_levels_variable": "srx_cpu_re_default_levels",
    "snmp_scan_function": srx_snmp_scan,
    "snmp_info": srx_cpu_snmp_info,
    "includes": ["juniper_srx.include"],
}
# pylint: enable=E0602
