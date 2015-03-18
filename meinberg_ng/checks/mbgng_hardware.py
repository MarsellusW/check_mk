#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK checks providing services for Meinberg LANTIME Timeserver hardware.

These checks handle firmware versions from v6 on.
"""

label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}

mbgng_scan = lambda oid: oid(".1.3.6.1.2.1.1.2.0") == ".1.3.6.1.4.1.5597.30"

factory_settings['mbgng_hw_default_levels'] = {  # pylint: disable=E0602
    "temperature": (60, 70),
}

mbgng_ps_state = {
    "0": "notAvailable",
    "1": "down",
    "2": "up",
}

mbgng_fan_state = {
    "0": "notAvailable",
    "1": "off",
    "2": "on",
}

mbgng_fan_error = {
    "0": "notAvailable",
    "1": "no",
    "2": "yes",
}

mbgng_hw_info = [
    ['.1.3.6.1.4.1.5597.30.0.5.0.2.1', [  # mbgLtNgSysPsTableEntry
        OID_END,  # pylint: disable=E0602
        2,  # mbgLtNgSysPsStatus
    ]],
    ['.1.3.6.1.4.1.5597.30.0.5.1.2.1', [  # mbgLtNgSysFanTableEntry
        OID_END,  # pylint: disable=E0602
        2,  # mbgLtNgSysFanStatus
        3,  # mbgLtNgSysFanError#
    ]],
    ['.1.3.6.1.4.1.5597.30.0.5.2', ['1.0']],  # mbgLtNgSysTempCelsius
]


# PowerSupply check

def inventory_mbgng_hardware_power(info):
    """Return inventory data for PowerSupplies."""
    inventory = []

    if info[0] is not None:
        for line in info[0]:
            inventory.append((line[0], "mbgng_hw_default_levels"))

    return inventory


def check_mbgng_hardware_power(item, _no_params, info):
    """Return check data for PowerSupplies."""
    if info[0] is not None:
        for line in info[0]:
            if line[0] == item:
                state = 0
                ps_state = mbgng_ps_state.get(line[1], "UNKNOWN")

                if ps_state == "down":
                    state = 2
                elif ps_state in ["notAvailable", "UNKNOWN"]:
                    state = 3

                return (state, "State is %s%s" % (ps_state, label[state]))

    return (3, "No data received")

# pylint: disable=E0602
check_info['mbgng_hardware.power'] = {
    "check_function": check_mbgng_hardware_power,
    "inventory_function": inventory_mbgng_hardware_power,
    "has_perfdata": False,
    "service_description": "LANTIME PowerSupply %s",
    "group": 'mbgng_hw',
    "default_levels_variable": "mbgng_hw_default_levels",
    "snmp_scan_function": mbgng_scan,
    "snmp_info": mbgng_hw_info,
}
# pylint: enable=E0602


# Fan check

def inventory_mbgng_hardware_fans(info):
    """Return inventory data for Fans."""
    inventory = []

    if info[1] is not None:
        for line in info[1]:
            inventory.append((line[0], "mbgng_hw_default_levels"))

    return inventory


def check_mbgng_hardware_fans(item, _no_params, info):
    """Return check data for Fans."""
    if info[1] is not None:
        for line in info[1]:
            if line[0] == item:
                state = 0
                fan_state = mbgng_fan_state.get(line[1], "UNKNOWN")
                fan_error = mbgng_fan_error.get(line[2], "UNKNOWN")

                if fan_state == "off":
                    state = 2
                elif fan_state in ["notAvailable", "UNKNOWN"]:
                    state = 3

                return (state, "State is %s%s, Error is '%s'" % (
                                fan_state, label[state], fan_error))

    return (3, "No data received")

# pylint: disable=E0602
check_info['mbgng_hardware.fans'] = {
    "check_function": check_mbgng_hardware_fans,
    "inventory_function": inventory_mbgng_hardware_fans,
    "has_perfdata": False,
    "service_description": "LANTIME Fan %s",
    "group": 'mbgng_hw',
    "default_levels_variable": "mbgng_hw_default_levels",
    "snmp_scan_function": mbgng_scan,
    "snmp_info": mbgng_hw_info,
}
# pylint: enable=E0602


# Temperature check

def inventory_mbgng_hardware_temp(info):
    """Return inventory data for Temperature."""
    if info[2] is not None:
        return [(None, "mbgng_hw_default_levels")]


def check_mbgng_hardware_temp(_no_item, params, info):
    """Return temperature data."""
    if info[2] is not None:
        state = 0
        warn, crit = params["temperature"]
        
        temp = int(info[2][0][0])
        
        state = 2 if temp > crit else 1 if temp > warn else 0

        perfdata = [("temp", temp, warn, crit)]

        return (state, "Temperature is %d°C" % temp, perfdata)
        
    return (3, "No data received")

# pylint: disable=E0602
check_info['mbgng_hardware.temp'] = {
    "check_function": check_mbgng_hardware_temp,
    "inventory_function": inventory_mbgng_hardware_temp,
    "has_perfdata": True,
    "service_description": "LANTIME Temperature",
    "group": 'mbgng_hw',
    "default_levels_variable": "mbgng_hw_default_levels",
    "snmp_scan_function": mbgng_scan,
    "snmp_info": mbgng_hw_info,
}
# pylint: enable=E0602
