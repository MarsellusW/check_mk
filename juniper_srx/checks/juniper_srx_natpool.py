#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK check providing a Service for NAT pools of Juniper SRX.
"""

factory_settings['srx_natpool_default_levels'] = {  # pylint: disable=E0602
    'if': (80.0, 100.0),
    'pat': (80.0, 100.0),
}

label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}

srx_natpool_type = {
    '1': "withPAT",
    '2': "withoutPAT",
    '3': "static",
}

srx_natpool_snmp_info = [
    ['.1.3.6.1.4.1.2636.3.39.1.7.1.1.3.1', [
        2,  # jnxJsNatIfSrcPoolTotalSinglePorts
        3,  # jnxJsNatIfSrcPoolAllocSinglePorts
        4,  # jnxJsNatIfSrcPoolTotalTwinPorts
        5,  # jnxJsNatIfSrcPoolAllocTwinPorts
        
    ]],
    ['.1.3.6.1.4.1.2636.3.39.1.7.1.1.4.1', [
        1,  # jnxJsNatSrcPoolName
        4,  # jnxJsNatSrcPoolType
        5,  # jnxJsNatSrcNumPortInuse (for pool type "withPAT")
        6,  # jnxJsNatSrcNumPortInuse (for other pool types)
    ]]
]


def parse_srx_natpool_info(params, values):
    """Parse natpool data."""
    current, allowed = [float(x) for x in values]
    util = current * 100 / allowed

    warn, crit = params

    perfdata = [("util", util, warn, crit, 0), ("allowed", allowed)]

    state = 2 if util >= crit else 1 if util >= warn else 0

    return (state, "%.2f%%%s utilized" % (util, label[state]), perfdata)


def inventory_srx_natpool(info):
    """Return natpool inventory data."""
    inventory = []

    if info is not None:
        for line in info:
            if int(line[6]) != 0:
                name = "%s FPC %s" % (line[0], line[1])
                inventory.append((name, "srx_sessions_default_levels"))

    return inventory


def check_srx_natpool(item, params, info):
    """Return natpool data."""
    for line in info:
        if int(line[6]) != 0:
            name = "%s FPC %s" % (line[0], line[1])

            if name == item:
                return(parse_srx_natpool_info(params["cp"], line[5:7]))

    return (3, "No data received for %s" % item)


# pylint: disable=E0602
check_info['juniper_srx_natpool'] = {
    "check_function": check_srx_natpool,
    "inventory_function": inventory_srx_natpool,
    "has_perfdata": True,
    "service_description": "NAT pool utilization %s",
    "group": 'srx_natpool_utilization',
    "default_levels_variable": "srx_natpool_default_levels",
    "snmp_scan_function": srx_snmp_scan,
    "includes": ["juniper_srx.include"],
}
# pylint: enable=E0602
