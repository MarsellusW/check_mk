#!/usr/bin/env python

#check_metrics["check_mk-speedtest"] = {
#    "download"  : { "unit" : "bits/s" },
#    "upload" : { "unit" : "bits/s" },
#    "ping" : { "unit" : "ms" }
#}

metric_info["download"] = {
        "title": "Download rate",
        "unit": "bits/s",
        "color": "34/a"
        }

metric_info["upload"] = {
        "title": "Upload rate",
        "unit": "bits/s",
        "color": "24/a"
        }
