#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# paloalto_cpu_default_levels = (80.0, 90.0)

state_label = {
            0: '',
            1: '(!)',
            2: '(!!)',
            3: '(!!!)',
            }

ironport_feature_default_levels = (20, 10)

ironport_esa_feature_state = {
            'Dormant/Perpetual': 0,
            }


def inventory_ironport_esa_features(info):
    return [(line[0], "ironport_feature_default_levels")
            for line in info]


def check_ironport_esa_features(item, params, info):
    for line in info:
        if line[0] == item:
            feature, remain = line

            warn, crit = map(int, params)

            state = 0
            msg = ""

            try:
                remain = int(remain)

                remain = remain / 24 / 3600
                if remain <= crit:
                    state = 2
                elif remain <= warn:
                    state = 1

                msg = "Expires in %d days%s" % (remain, state_label[state])

                if state > 0:
                    msg = "%s (levels at %d/%d)" % (msg, warn, crit)
            except ValueError, e:
                state = ironport_esa_feature_state.get(remain, 3)
                msg = "%s is %s%s" % (msg, remain, state_label[state])

            return (state, msg)

    return (3, "No data received for feature %s" % item)


# pylint: disable=E0602
check_info['ironport_esa_features'] = {
    "check_function"      : check_ironport_esa_features,
    "inventory_function"  : inventory_ironport_esa_features,
    "has_perfdata"        : False,
    "service_description" : "IronPort License %s",
}
# pylint: enable=E0602
