#!/usr/bin/python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

'''
cleanup_perfdata: remove perfdata files not needed anymore

This script removes perfdata files not needed anymore. The fileage threshold can
be defined in days and defaults to 90.

Script in intended to be run as cronjob or manually from commandline, both in an
OMD environment. If you do not use OMD the script will explain what changes are
needed.

Attention: set "CMS_IS_IN_USE = False" below if Check_MK Micro Core is not used!

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

import xml.etree.ElementTree as ET
import shutil
import time
import livestatus  # pylint: disable=E0401

__all__ = []
__version__ = 0.8
__date__ = '2015-08-12'
__updated__ = '2015-08-17'

# Modification time of files must be older that this number of days
# (defaults to 90)
XDAYS = 90

# Set this to False if Check_MK Micro Core is not in use, True otherwise
CMS_IS_IN_USE = True

try:
    omd_root = os.getenv("OMD_ROOT")
    socket_path = "unix:" + omd_root + "/tmp/run/live"
    perfdata_path = omd_root + "/var/pnp4nagios/perfdata"
except RuntimeError:
    sys.stderr.write("This script is indented to run in an OMD site\n")
    sys.stderr.write("Please change socket_path and perfdata_path above,\n")
    sys.stderr.write("if you are not using OMD.\n")
    sys.exit(1)

now = time.time()
VERBOSE = False
DRYRUN = False

DELETED = {
    'folders': 0,
    'xmlfiles': 0,
    'rrdfiles': 0,
}

KEPT = {
    'xmlfiles': 0,
    'rrdfiles': 0,
}


def p_out(msg):
    """
    Print out msg.
    """
    if DRYRUN:
        msg = f"dryrun: {msg}"

    if VERBOSE:
        print(msg)


def get_livestatus_data(query):
    """
    Prepare livestatus query single site connection and give query.
    """
    try:
        return livestatus.SingleSiteConnection(socket_path).query_table(query)
    except RuntimeError as run_error:  # livestatus.MKLivestatusException, e:
        print(f"Livestatus error: {str(run_error)}")
        sys.exit(1)


def search_files(host_path):
    """
    Search all files and old files recursively in the given host_path.
    """
    all_files = {}
    old_files = {}

    for root, _, files in os.walk(host_path):
        for name in files:
            filename = os.path.join(root, name)
            file_ext = os.path.splitext(filename)[1][1:].lower()

            if CMS_IS_IN_USE:  # path starts with /opt/omd instead of /omd
                filename = f"/opt{filename}"

            all_files.setdefault(file_ext, {})[filename] = True

            if os.stat(filename).st_mtime < now - (XDAYS * 86400):
                if file_ext in ['xml', 'rrd']:
                    old_files.setdefault(file_ext, {})[filename] = True
                    p_out(f"File {filename} is too old")

    return all_files, old_files


def process_xml_files(host, all_files, old_files):
    """
    Process xml files by searching if the service of host is still in the xml file
    for this host and delete or keep accordingly.
    """
    query_svcs = "GET services\nColumns: description host_name"
    query_svcs += f"\nFilter: host_name = {host}"

    svcs = {}

    for svc, _host in get_livestatus_data(query_svcs):
        svcs[svc] = True

    for xmlfile in old_files['xml']:
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        svc = root.find("NAGIOS_AUTH_SERVICEDESC").text

        if svc not in svcs:
            p_out(f"service '{svc}' of old xml '{xmlfile}' not found, deleting xml")

            del all_files['xml'][xmlfile]
            DELETED['xmlfiles'] += 1

            if not DRYRUN:
                os.remove(xmlfile)
        else:
            p_out(f"service '{svc}' of old xml '{xmlfile}' still used, keeping xml")

            KEPT['xmlfiles'] += 1

    return all_files


def process_rrd_files(all_files, old_files):
    """
    Process rrd files by searching in the xml files for a RRDFILE entry and see if rrd file
    is part of it and delete or keep accordingly.
    """

    rrdref = {}
    for xmlfile in all_files['xml']:
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        for data_source in root.findall('DATASOURCE'):
            rrdfile = data_source.find('RRDFILE').text
            rrdref[rrdfile] = True

    for rrdfile in old_files['rrd']:
        if rrdfile not in rrdref:
            p_out(f"old rrd '{rrdfile}' not needed anymore, deleting rrd")

            DELETED['rrdfiles'] += 1

            if not DRYRUN:
                os.remove(rrdfile)
        else:
            p_out(f"old rrd '{rrdfile}' still needed, keeping rrd")

            KEPT['rrdfiles'] += 1


def get_hosts():
    """
    Get all hostnames and aliases over the livestatus socket of Checkmk.
    """
    query_hosts = "GET hosts\nColumns: name alias"

    hosts = {}

    for host, _alias in get_livestatus_data(query_hosts):
        hosts[host] = True

    return hosts


def process_host(host, hosts):
    """
    Check for the host to not be in hosts and deletes the host file according to that.
    Otherwise check for xml files and rrd files which can be processed.
    """
    skip_hosts = ['.pnp-internal']
    host_path = perfdata_path + "/" + host

    if host not in hosts and host not in skip_hosts:
        p_out(f"Host '{host}' does not exist (anymore), deleting folder")

        DELETED['folders'] += 1

        if not DRYRUN:
            shutil.rmtree(host_path)

    else:  # search for files too old
        all_files, old_files = search_files(host_path)

        if old_files.get('xml', None):
            all_files = process_xml_files(host, all_files, old_files)

        if old_files.get('rrd', None):
            process_rrd_files(all_files, old_files)


def print_statistics():
    """
    Print statistics of the files which are processed.
    """
    print(f"folders deleted:\t{DELETED['folders']}")

    for filetype in ["xmlfiles", "rrdfiles"]:
        print(f"{filetype} deleted:\t{DELETED[filetype]}")
        print(f"{filetype} kept:   \t{KEPT[filetype]}")


def init(argv=None):
    """
    Init function to parse all options and arguments of the script.
    """
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = f"v{__version__}"
    program_build_date = str(__updated__)
    program_version_message = f'{program_version} ({program_build_date})'
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = f'''{program_shortdesc}

  Created by Marcel Schulte (schulte.marcel@gmail.com) on str(__date__).
  Copyright 2015 Marcel Schulte. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
'''

    local_verbose = None
    local_dryrun = None
    local_xdays = None

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            "-x",
            "--xdays",
            dest="XDAYS",
            type=int,
            default=XDAYS,
            help="set fileage in days [default: %(default)s]")
        parser.add_argument(
            "-n",
            "--dryrun",
            dest="DRYRUN",
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
            dest="VERBOSE",
            action="store_true",
            help="set verbosity level [default: %(default)s]")
        parser.add_argument(
            '-V',
            '--version',
            action='version',
            version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        local_verbose = args.VERBOSE
        local_dryrun = args.DRYRUN
        local_xdays = args.XDAYS

        if args.DRYRUN:
            local_verbose = True
            print("Dryrun mode on")

        if args.drynonverb:
            local_dryrun = True
            print("Dryrun mode on")
            print("Verbose mode off")

        if args.VERBOSE:
            print("Verbose mode on")

        p_out(f"search and delete files older than {str(XDAYS)} days")
    except KeyboardInterrupt:
        # handle keyboard interrupt #
        return 0
    except RuntimeError as runtime_error:
        if local_dryrun or local_verbose:
            raise runtime_error
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(runtime_error) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    return (local_verbose, local_dryrun, local_xdays)


def main():  # IGNORE:C0111
    """
    Gather all hosts and process their paths.
    """
    print(f"starting at {str(now)}")

    hosts = get_hosts()

    for host in next(os.walk(perfdata_path))[1]:
        process_host(host, hosts)

    print_statistics()

    return 0


if __name__ == "__main__":
    init_values = init()
    if isinstance(init_values, int):
        sys.exit(init_values)
    else:
        (VERBOSE, DRYRUN,  XDAYS) = init_values
    sys.exit(main())
