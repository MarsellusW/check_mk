#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

'''
cleanup_perfdata: remove perfdata files not needed anymore

This script removes perfdata files not needed anymore. The fileage threshold can
be defined in days and defaults to 90.

Script in intended to be run as cronjob or manually from commandline, both in an
OMD environment. If you do not use OMD the script will explain what changes are
needed.

Attention: set "cmc_is_in_use = False" below if Check_MK Micro Core is not used!

It defines classes_and_methods

@author:     Marcel Schulte

@copyright:  2015 Marcel Schulte. All rights reserved.

@license:    Apache License 2.0

@contact:    schulte.marcel@gmail.com
@deffield    updated: 2015-08-17
'''

import os
import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import livestatus
import xml.etree.ElementTree as ET
import shutil
import time

__all__ = []
__version__ = 0.8
__date__ = '2015-08-12'
__updated__ = '2015-08-17'

# Modification time of files must be older that this number of days
# (defaults to 90)
xdays = 90

# Set this to False if Check_MK Micro Core is not in use, True otherwise
cmc_is_in_use = True

try:
    omd_root = os.getenv("OMD_ROOT")
    socket_path = "unix:" + omd_root + "/tmp/run/live"
    perfdata_path = omd_root + "/var/pnp4nagios/perfdata"
except:
    sys.stderr.write("This script is indented to run in an OMD site\n")
    sys.stderr.write("Please change socket_path and perfdata_path above,\n")
    sys.stderr.write("if you are not using OMD.\n")
    sys.exit(1)

now = time.time()
verbose = False
dryrun = False

deleted = {
    'folders': 0,
    'xmlfiles': 0,
    'rrdfiles': 0,
}

kept = {
    'xmlfiles': 0,
    'rrdfiles': 0,
}


def p_out(msg):
    if dryrun:
        msg = "DRYRUN: %s" % msg

    if verbose:
        print msg

    return


def get_livestatus_data(query):
    try:
        return livestatus.SingleSiteConnection(socket_path).query_table(query)
    except Exception as e:  # livestatus.MKLivestatusException, e:
        print "Livestatus error: %s" % str(e)
        sys.exit(1)


def search_files(host_path):
    all_files = {}
    old_files = {}

    for root, dirs, files in os.walk(host_path):
        for name in files:
            filename = os.path.join(root, name)
            file_ext = os.path.splitext(filename)[1][1:].lower()

            if cmc_is_in_use:  # path starts with /opt/omd instead of /omd
                filename = "/opt%s" % filename

            all_files.setdefault(file_ext, {})[filename] = True

            if os.stat(filename).st_mtime < now - (xdays * 86400):
                if file_ext in ['xml', 'rrd']:
                    old_files.setdefault(file_ext, {})[filename] = True
                    p_out("File %s is too old" % filename)

    return all_files, old_files


def process_xml_files(host, all_files, old_files):
    global deleted
    global kept

    query_svcs = "GET services\nColumns: description host_name"
    query_svcs += "\nFilter: host_name = %s" % host

    svcs = {}

    for svc, _host in get_livestatus_data(query_svcs):
        svcs[svc] = True

    for xmlfile in old_files['xml']:
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        svc = root.find("NAGIOS_AUTH_SERVICEDESC").text

        if svc not in svcs:
            p_out("service '%s' of old xml '%s' not found, deleting xml" % (
                svc, xmlfile))

            del(all_files['xml'][xmlfile])
            deleted['xmlfiles'] += 1

            if not dryrun:
                os.remove(xmlfile)
        else:
            p_out("service '%s' of old xml '%s' still used, keeping xml" % (
                svc, xmlfile))

            kept['xmlfiles'] += 1

    return all_files


def process_rrd_files(host, all_files, old_files):
    global deleted
    global kept

    rrdref = {}
    for xmlfile in all_files['xml']:
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        for ds in root.findall('DATASOURCE'):
            rrdfile = ds.find('RRDFILE').text
            rrdref[rrdfile] = True

    for rrdfile in old_files['rrd']:
        if rrdfile not in rrdref:
            p_out("old rrd '%s' not needed anymore, deleting rrd" % rrdfile)

            deleted['rrdfiles'] += 1

            if not dryrun:
                os.remove(rrdfile)
        else:
            p_out("old rrd '%s' still needed, keeping rrd" % rrdfile)

            kept['rrdfiles'] += 1

    return


def get_hosts():
    query_hosts = "GET hosts\nColumns: name alias"

    hosts = {}

    for host, _alias in get_livestatus_data(query_hosts):
        hosts[host] = True

    return hosts


def process_host(host, hosts):
    global deleted

    host_path = perfdata_path + "/" + host

    if host not in hosts:
        # host does not exist (anymore), delete regardless of file age
        p_out("Host '%s' does not exist (anymore), deleting folder" % host)

        deleted['folders'] += 1

        if not dryrun:
            shutil.rmtree(host_path)

    else:  # search for files too old
        all_files, old_files = search_files(host_path)

        if old_files.get('xml', None):
            all_files = process_xml_files(host, all_files, old_files)

        if old_files.get('rrd', None):
            process_rrd_files(host, all_files, old_files)

    return


def print_statistics():
    print("folders deleted:\t%6d" % deleted['folders'])

    for st in ["xmlfiles", "rrdfiles"]:
        print("%s deleted:\t%6d" % (st, deleted[st]))
        print("%s kept:   \t%6d" % (st, kept[st]))

    return


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    global verbose
    global dryrun
    global xdays

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Marcel Schulte (schulte.marcel@gmail.com) on %s.
  Copyright 2015 Marcel Schulte. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            "-x",
            "--xdays",
            dest="xdays",
            type=int,
            default=xdays,
            help="set fileage in days [default: %(default)s]")
        parser.add_argument(
            "-n",
            "--dryrun",
            dest="dryrun",
            action="store_true",
            help="do not delete anything, just report [default: %(default)s]")
        parser.add_argument(
            "-N",
            dest="drynonverb",
            action="store_true",
            help="'dryrun' but non-verbose, just stats [default: %(default)s]")
        parser.add_argument(
            "-v",
            "--verbose",
            dest="verbose",
            action="store_true",
            help="set verbosity level [default: %(default)s]")
        parser.add_argument(
            '-V',
            '--version',
            action='version',
            version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        dryrun = args.dryrun
        drynonverb = args.drynonverb
        xdays = args.xdays

        if dryrun:
            verbose = True
            print("Dryrun mode on")

        if drynonverb:
            dryrun = True
            print("Dryrun mode on")
            print("Verbose mode off")

        if verbose:
            print("Verbose mode on")

        p_out("search and delete files older than %s days" % str(xdays))

        # MAIN BODY #
        print "starting at %s" % str(now)

        hosts = get_hosts()

        for host in next(os.walk(perfdata_path))[1]:
            process_host(host, hosts)

        print_statistics()

        return 0

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if dryrun or verbose:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())
