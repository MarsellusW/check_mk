#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

"""
Check_MK checks providing services for Meinberg LANTIME Timeservers.

These checks handle firmware versions from v6 on.
"""
label = {
    0: "",
    1: "(!)",
    2: "(!!)",
    3: "(!!!)"
}

mbgng_scan = lambda oid: oid(".1.3.6.1.2.1.1.2.0") == ".1.3.6.1.4.1.5597.30"

factory_settings['mbgng_ntp_default_levels'] = {  # pylint: disable=E0602
    'stratum': (1, 1),
    'offset': (500, 1000),
}

mbgng_ntp_state = {
    '0': 'notAvailable',
    '1': 'notSynchronized',
    '2': 'synchronized',
}

def inventory_mbgng_ntp(info):
    """Return inventory data for NTP."""
    if info is not None:
    #if len(info) > 0 and len(info[0]) == 4:
        return [(None, None, "mbgng_ntp_default_levels")]

def check_mbgng_ntp(_no_item, params, info):
    """Return check data for NTP."""
    if info is not None:
        ntp_state, stratum, refclock_name, refclock_offset = info[0]

        state = 0
        msg = []

        # Handle the reported state
        lbl = ''
        
        if ntp_state in ['0', '1']:
            state = max(state, 2)
            lbl = label[2]
        
        msg.append(
            'State: %s%s' % (
                mbgng_ntp_state.get(ntp_state, 'UNKNOWN'),
                lbl
            )
        )

        # handle the reported stratum
        lbl = ''
        warn, crit = params["stratum"]

        if int(stratum) > crit:
            state = max(state, 2)
            lbl = label[2]
        elif int(stratum) > warn:
            state = max(state, 1)
            lbl = label[1]

        msg.append('Stratum: %s%s' % (stratum, lbl))

        # Add refclock information
        msg.append('Refclock: %s' % refclock_name)

        lbl = ''
        warn, crit = params["offset"]

        rc_offset = abs(savefloat(refclock_offset))  # pylint: disable=E0602

        if rc_offset > crit:
            state = max(state, 2)
            lbl = label[2]
        elif rc_offset > warn:
            state = max(state, 1)
            lbl = label[1]

        msg.append(
            'Refclock offset: %0.4fms%s' % (
                savefloat(refclock_offset) / 1000,  # pylint: disable=E0602
                lbl
            )
        )

        perfdata = [('offset', refclock_offset, warn, crit)]

        return (state, ", ".join(msg), perfdata)

    return (3, 'Got no state information')

# pylint: disable=E0602
check_info['mbgng_ntp'] = {
    "check_function": check_mbgng_ntp,
    "inventory_function": inventory_mbgng_ntp,
    "has_perfdata": True,
    "service_description": "LANTIME NTP",
    "group": 'mbgng_ntp',
    "default_levels_variable": "mbgng_ntp_default_levels",
    "snmp_scan_function": mbgng_scan,
    "snmp_info": ('.1.3.6.1.4.1.5597.30.0.2', [
        1,  # mbgLtNgNtpCurrentState
        2,  # mbgLtNgNtpStratum
        3,  # mbgLtNgNtpRefclockName
        4,  # mbgLtNgNtpRefclockOffset
    ]),
}
# pylint: enable=E0602
