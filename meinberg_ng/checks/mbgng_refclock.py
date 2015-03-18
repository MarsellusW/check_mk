#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK checks providing services for Meinberg LANTIME Timeserver refclocks.

These checks handle firmware versions from v6 on.
"""

import re

label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}

mbgng_scan = lambda oid: oid(".1.3.6.1.2.1.1.2.0") == ".1.3.6.1.4.1.5597.30"

factory_settings['mbgng_rc_default_levels'] = {  # pylint: disable=E0602
    "satellites": (4, 3),
}

mbgng_rc_state = {
    "0": "notAvailable",
    "1": "synchronized",
    "2": "notSynchronized",
}

mbgng_rc_substate = {
    "0": "notAvailable",
    "1": "gpsSync",
    "2": "gpsTracking",
    "3": "gpsAntennaDisconnected",
    "4": "gpsWarmBoot",
    "5": "gpsColdBoot",
    "6": "gpsAntennaShortCircuit",
    "50": "lwNeverSync",
    "51": "lwNotSync",
    "52": "lwSync",
    "100": "tcrNotSync",
    "101": "tcrSync",
}

mbgng_rc_type = {
    "0": "unknown",
    "1": "gps166",
    "2": "gps167",
    "3": "gps167SV",
    "4": "gps167PC",
    "5": "gps167PCI",
    "6": "gps163",
    "7": "gps168PCI",
    "8": "gps161",
    "9": "gps169PCI",
    "10": "tcr167PCI",
    "11": "gps164",
    "12": "gps170PCI",
    "13": "pzf511",
    "14": "gps170",
    "15": "tcr511",
    "16": "am511",
    "17": "msf511",
    "18": "grc170",
    "19": "gps170PEX",
    "20": "gps162",
    "21": "ptp270PEX",
    "22": "frc511PEX",
    "23": "gen170",
    "24": "tcr170PEX",
    "25": "wwvb511",
    "26": "mgr170",
    "27": "jjy511",
    "28": "pzf600",
    "29": "tcr600",
    "30": "gps180",
    "31": "gln170",
    "32": "gps180PEX",
    "33": "tcr180PEX",
    "34": "pzf180PEX",
    "35": "mgr180",
    "36": "msf600",
    "37": "wwvb600",
    "38": "jjy600",
    "39": "gps180HS",
    "40": "gps180AMC",
    "41": "esi180",
    "42": "cpe180",
    "43": "lno180",
    "44": "grc180",
    "45": "liu",
    "46": "dcf600HS",
    "47": "dcf600RS",
}

mbgng_rc_usage = {
    "0": "notAvailable",
    "1": "secondary",
    "2": "compare",
    "3": "primary",
}

mbgng_rc_typestate = {
    "gps": [1, 2, 3, 4, 5, 6],
    "lw": [50, 51, 52],
    "irig": [100, 101],
}
mbgng_rc_info = [
    ['.1.3.6.1.4.1.5597.30.0.1.2.1', [
        OID_END,  # pylint: disable=E0602
        2,  # mbgLtNgRefclockType
        3,  # mbgLtNgRefclockUsage
        4,  # mbgLtNgRefclockState
        5,  # mbgLtNgRefclockSubstate
        6,  # mbgLtNgRefclockStatusA
        7,  # mbgLtNgRefclockMaxStatusA
        8,  # mbgLtNgRefclockStatusB
        9,  # mbgLtNgRefclockMaxStatusB
        10,  # mbgLtNgRefclockAdditionalInfo
        11,  # mbgLtNgRefclockLeapSecondDate
    ]],
    ['.1.3.6.1.4.1.5597.30.0.1', ["5.0"]]  # mbgLtNgRefclockGpsPos
]


def mbgng_parse_refclock_info(line):
    """Parse data from info line and return dictionary."""
    data = {}

    params = [
        "item",
        "type",
        "usage",
        "state",
        "substate",
        "state_a",
        "max_a",
        "state_b",
        "max_b",
        "add_info",
        "leap_date"
    ]

    for idx, param in enumerate(params):
        data[param] = line[idx]

    return data


def inventory_mbgng_refclock(info):
    """Return inventory data for each refclock."""
    inventory = []

    if info[0] is not None:
        for line in info[0]:
            inventory.append((line[0], "mbgng_rc_default_levels"))

    return inventory


def check_mbgng_refclock(item, params, info):
    """Return check data for each refclock."""
    for line in info[0]:
        if line[0] == item:
            data = mbgng_parse_refclock_info(line)

            state = 0
            lbl = ""
            msg = []

            perfdata = []

            # Handle refclock states
            if data["state"] == "0":
                state = max(state, 2)
                lbl = label[2]
            elif data["state"] == "2":
                state = max(state, 1)
                lbl = label[1]

            msg.append(
                "State: %s (%s)%s" % (
                    mbgng_rc_state.get(data["state"], "UNKNOWN"),
                    mbgng_rc_substate.get(data["substate"], "UNKNOWN"),
                    lbl
                )
            )

            msg.append("Type: %s" % mbgng_rc_type.get(data["type"], "UNKNOWN"))
            msg.append("Usage: %s" % mbgng_rc_usage.get(
                data["usage"], "UNKNOWN")
            )

            # Check generic type of refclock
            if int(data["substate"]) in mbgng_rc_typestate["gps"]:
                lbl = ""
                warn, crit = params["satellites"]

                if int(data["state_a"]) <= crit:
                    state = max(state, 2)
                    lbl = label[2]
                elif int(data["state_a"]) <= warn:
                    state = max(state, 1)
                    lbl = label[1]

                perfdata = [('sat_good', data["state_a"], warn, crit),
                            ('sat_total', data["max_a"])]

                msg.append(
                    "Satellites: %s/%s%s" % (
                        data["state_a"],
                        data["max_a"],
                        lbl
                    )
                )

                msg.append(info[1][0][0])  # GPS position
            elif re.match("pzf",
                          mbgng_rc_type[data["type"]],
                          flags=re.I):
                msg.append(
                    "Correlation: %s%%" % data["state_a"]
                )

            if int(data["substate"]) in mbgng_rc_typestate["lw"]:
                msg.append(
                    "Field strength: %s%%" % data["state_b"]
                )

            if data["add_info"] == "1":
                msg.append(
                    "Leap second date: %s" % data["leap_date"]
                )

            return(state, ", ".join(msg), perfdata)

    return (3, "No data received for refclock %s" % item)

# pylint: disable=E0602
check_info['mbgng_refclock'] = {
    "check_function": check_mbgng_refclock,
    "inventory_function": inventory_mbgng_refclock,
    "has_perfdata": True,
    "service_description": "LANTIME Refclock %s",
    "group": 'mbgng_rc',
    "default_levels_variable": "mbgng_rc_default_levels",
    "snmp_scan_function": mbgng_scan,
    "snmp_info": mbgng_rc_info,
}
# pylint: enable=E0602
