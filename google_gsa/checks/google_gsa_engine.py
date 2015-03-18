#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

google_gsa_crawl_status = {
                     0: "paused",
                     1: "running",
                    }

gsa_snmp_scan = lambda oid: "GSA Version" in oid(".1.3.6.1.2.1.1.1.0")

gsa_engine_snmp_info = [
                        (".1.3.6.1.4.1.11129.1.2", [1]),
                        (".1.3.6.1.4.1.11129.1.1", [1, 2]),
                       ]

def inventory_google_gsa_engine(info):
    if info:
        return [(None, None)]

def check_google_gsa_engine(_item, _params, info):
    if info:
        query_per_min = info[0][0][0]
        crawl_status = google_gsa_crawl_status[int(info[1][0][0])]
        doc_served, crawl_rate, doc_bytes, today_crawled, doc_errors, doc_found = [y for x, y in info[1][1:7]]
        
        perfdata = []
        perfdata.append(("bytes", doc_bytes))
        perfdata.append(("served", doc_served))
        perfdata.append(("found", doc_found))
        perfdata.append(("today", today_crawled))
        perfdata.append(("rate", crawl_rate))
        perfdata.append(("queryrate", query_per_min))
        perfdata.append(("errors", doc_errors))

        return 0, "crawling is \"%s\", %s bytes processed, serving %s of %s found docs, %s docs crawled today, crawl rate is %s, %s queries/min, %s errors occurred crawling" % (crawl_status, doc_bytes, doc_served, doc_found, today_crawled, crawl_rate, query_per_min, doc_errors), perfdata

        if errtxt:
            errtxt = ", reported error is \"%s\"" % errtxt

        txt, label = google_gsa_status[int(status)]

        return int(status), "reported status is \"%s\"%s%s" % (txt, label, errtxt)
    else:
        return 3, "Item not found in SNMP data"

check_info['google_gsa_engine'] = {
    "check_function"      : check_google_gsa_engine,
    "inventory_function"  : inventory_google_gsa_engine,
    "has_perfdata"        : True,
    "service_description" : "GSA engine",
    "snmp_scan_function"  : gsa_snmp_scan,
    "snmp_info"           : gsa_engine_snmp_info,
}
