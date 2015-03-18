#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK check providing a Service for Session Counts of Juniper SRX.
"""

factory_settings['srx_sessions_default_levels'] = {  # pylint: disable=E0602
    'cp': (80.0, 90.0),
    'flow': (80.0, 90.0),
}

label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}

srx_sessions_snmp_info = ('.1.3.6.1.4.1.2636.3.39.1.12.1.1.1', [
    11,  # jnxJsSPUMonitoringNodeDescr
    2,  # jnxJsSPUMonitoringFPCIndex
    3,  # jnxJsSPUMonitoringSPUIndex
    6,  # jnxJsSPUMonitoringCurrentFlowSession
    7,  # jnxJsSPUMonitoringMaxFlowSession
    8,  # jnxJsSPUMonitoringCurrentCPSession
    9,  # jnxJsSPUMonitoringMaxCPSession
])


def parse_srx_session_info(params, values):
    """Parse session data."""
    current, allowed = [float(x) for x in values]
    util = current * 100 / allowed

    warn, crit = params

    perfdata = [("util", util, warn, crit, 0), ("allowed", allowed)]

    state = 2 if util >= crit else 1 if util >= warn else 0

    return (state, "%.2f%%%s utilized" % (util, label[state]), perfdata)


def inventory_srx_cp_sessions(info):
    """Return CP session inventory data."""
    inventory = []

    if info is not None:
        for line in info:
            if int(line[6]) != 0:
                name = "%s FPC %s" % (line[0], line[1])
                inventory.append((name, "srx_sessions_default_levels"))

    return inventory


def check_srx_cp_sessions(item, params, info):
    """Return CP session data."""
    for line in info:
        if int(line[6]) != 0:
            name = "%s FPC %s" % (line[0], line[1])

            if name == item:
                return(parse_srx_session_info(params["cp"], line[5:7]))

    return (3, "No data received for %s" % item)


# pylint: disable=E0602
check_info['juniper_srx_sessions.cp'] = {
    "check_function": check_srx_cp_sessions,
    "inventory_function": inventory_srx_cp_sessions,
    "has_perfdata": True,
    "service_description": "Sessions (CP) utilization %s",
    "group": 'srx_sessions_utilization',
    "default_levels_variable": "srx_sessions_default_levels",
    "snmp_scan_function": srx_snmp_scan,
    "snmp_info": srx_sessions_snmp_info,
    "includes": ["juniper_srx.include"],
}
# pylint: enable=E0602


def inventory_srx_flow_sessions(info):
    """Return Flow session inventory data."""
    inventory = []

    if info is not None:
        for line in info:
            if int(line[4]) != 0:
                name = "%s FPC %s/SPU %s" % (line[0], line[1], line[2])
                inventory.append((name, "srx_sessions_default_levels"))

    return inventory


def check_srx_flow_sessions(item, params, info):
    """Return Flow session data."""
    for line in info:
        node, fpc, spu = line[0:3]
        name = "%s FPC %s/SPU %s" % (node, fpc, spu)

        if name == item:
            if int(line[4]) != 0:
                return(parse_srx_session_info(params["cp"], line[3:5]))

    return (3, "No data received for %s" % item)


# pylint: disable=E0602
check_info['juniper_srx_sessions.flow'] = {
    "check_function": check_srx_flow_sessions,
    "inventory_function": inventory_srx_flow_sessions,
    "has_perfdata": True,
    "service_description": "Sessions (Flow) utilization %s",
    "group": 'srx_sessions_utilization',
    "default_levels_variable": "srx_sessions_default_levels",
    "snmp_scan_function": srx_snmp_scan,
    "snmp_info": srx_sessions_snmp_info,
    "includes": ["juniper_srx.include"],
}
# pylint: enable=E0602
