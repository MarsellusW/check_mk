#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# IronPort ESA poller agent

if __name__ == '__main__':
    import requests
    import sys
    import getopt
    import time
    import getpass
    from xml.dom import minidom
    import traceback
    import optparse
    import socket
    import re

    socket.setdefaulttimeout(10)

    usage = "usage: %prog [options] host"
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("-u", "--user", default = "admin",
        help = "User to authenticate as.  Default: admin")
    opt_parser.add_option("-p", "--passwd", default = "",
        help = "Password to authenticate with.")
    opt_parser.add_option("-r", "--realm", default = "IronPort Web Interface",
            help = "HTTP Realm to authenticate in.  Defaults to: " \
                 "IronPort Web Interface")

    try:
        (opt, args) = opt_parser.parse_args()
        host = args[0]
    except optparse.OptParseError:
        print "Error: Invalid command line parameters."
        opt_parser.print_help()
        traceback.print_exc()
        sys.exit(2)
    except IndexError:
        print "Error: No host provided."
        opt_parser.print_help()
        sys.exit(2)

    data = {}
    
    for xml in ["status", "dnsstatus"]:
        try:
            client = requests.get("https://%s/xml/%s" % (host, xml), auth=(opt.user, opt.passwd), verify=False)
        except Exception, e:
            print "HTTPS fehlgeschlagen! %s" % e
            traceback.print_exc()
            sys.exit(2)
        data[xml] = client.text
    dom = minidom.parseString(data['status'])

    version = '0.1'
    device = 'IronPort AsyncOS'

    sys.stdout.write('<<<check_mk>>>\n')
    sys.stdout.write('Version: %s\n' % version)
    sys.stdout.write('AgentOS: %s\n' % device)

    # gather & print feature info.
    feature_group = dom.getElementsByTagName("features")[0]
    features = feature_group.getElementsByTagName("feature")
    sys.stdout.write("<<<ironport_esa_features>>>\n")
    for feature in features:
        sys.stdout.write("%s %s\n" % (re.sub(r"\s+", '_', feature.attributes["name"].value),
                         feature.attributes["time_remaining"].value))

    # gather & print gauge info
    gauge_group = dom.getElementsByTagName("gauges")[0]
    gauges = gauge_group.getElementsByTagName("gauge")
    sys.stdout.write("<<<ironport_esa_gauges>>>\n")
    for gauge in gauges:
        sys.stdout.write("%s %s\n" % (re.sub(r"\s+", '_', gauge.attributes["name"].value),
                         gauge.attributes["current"].value))

    sys.stdout.write("<<<ironport_esa_counters>>>\n")

    for xml in ["status", "dnsstatus"]:
        dom = minidom.parseString(data[xml])
        counter_group = dom.getElementsByTagName("counters")[0]
        counters = counter_group.getElementsByTagName("counter")
        for counter in counters:
            sys.stdout.write("%s %s\n" % (re.sub(r"\s+", '_', counter.attributes["name"].value),
                                          counter.attributes["lifetime"].value))

