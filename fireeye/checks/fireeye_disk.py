#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#import locale
#locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

def inventory_fireeye_disk(info):
    if info:
        inventory = []

        for (name, status_txt, healthy, size_mbytes) in info:
            inventory.append((name, None))

        return inventory

def check_fireeye_disk(item, _params, info):
    for line in info:
        name, status_txt, healthy, size_mbytes = line

        if name == item:
            rc = 0

            label = ''
            msgtxt = 'healthy'
            healthy = fireeye_truefalse[healthy]
#            size_mbytes = locale.atoi(size_mbytes)
            size_mbytes = int(re.sub(r'\.', '', size_mbytes))
            size_gbytes = size_mbytes / 1024.0

            if not healthy:
                rc = 1
                label = '(!)'
                msgtxt = "un%s" % msgtxt

            return rc, "Disk %s is %s (\"%s\")%s, size is %d MB/%.2f GB" % (name, msgtxt, status_txt, label, size_mbytes, size_gbytes)

    return 3, "item not found in SNMP data"

check_info["fireeye_disk"] = {
    "check_function"      : check_fireeye_disk,
    "inventory_function"  : inventory_fireeye_disk,
    "has_perfdata"        : False,
    "service_description" : "FE Disk %s",
    "snmp_info"           : (".1.3.6.1.4.1.25597.11.2.1.3.1", [ 2, 3, 4, 7 ]),
    "snmp_scan_function"  : fireeye_snmp_scan,
    "includes"            : [ "fireeye.include" ],
}

