<?php
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2013             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

setlocale(LC_ALL, "C");

$ds_name[1] = 'Bytes processed';
$opt[1] = "--vertical-label \"bytes\" -b 1024 --title \"Bytes processed $hostname / $servicedesc\" ";
$def[1] =
  "DEF:bytes=$RRDFILE[1]:$DS[1]:MAX ".
  "AREA:bytes#00e060:\"bytes        \" ".
  "GPRINT:bytes:LAST:\"%7.1lf %s last\" ".
  "GPRINT:bytes:AVERAGE:\"%7.1lf %s avg\" ".
  "GPRINT:bytes:MAX:\"%7.1lf %s max\\n\" ".
  "";

$ds_name[2] = 'Documents served';
$ds_name[3] = 'Documents found';
$opt[2] = "--vertical-label \"docs\" -b 1000 --title \"Document count $hostname / $servicedesc\" ";
$def[2] =
  "DEF:found=$RRDFILE[3]:$DS[3]:MAX ".
  "AREA:found#00e060:\"found        \" ".
  "GPRINT:found:LAST:\"%7.1lf %s last\" ".
  "GPRINT:found:AVERAGE:\"%7.1lf %s avg\" ".
  "GPRINT:found:MAX:\"%7.1lf %s max\\n\" ".
  "DEF:served=$RRDFILE[2]:$DS[2]:MAX ".
  "AREA:served#0080e0:\"served       \" ".
  "GPRINT:served:LAST:\"%7.1lf %s last\" ".
  "GPRINT:served:AVERAGE:\"%7.1lf %s avg\" ".
  "GPRINT:served:MAX:\"%7.1lf %s max\\n\" ".
  "";

$ds_name[4] = 'Documents crawled today';
$opt[3] = "--vertical-label \"docs\" -b 1000 --title \"Documents crawled today $hostname / $servicedesc\" ";
$def[3] =
  "DEF:ctoday=$RRDFILE[4]:$DS[4]:MAX ".
  "AREA:ctoday#0060c0:\"docs crawled        \" ".
  "GPRINT:ctoday:LAST:\"%7.1lf %s last\" ".
  "GPRINT:ctoday:AVERAGE:\"%7.1lf %s avg\" ".
  "GPRINT:ctoday:MAX:\"%7.1lf %s max\\n\" ".
  "";

$ds_name[5] = 'Crawl rate';
$opt[4] = "--vertical-label \"crawl rate\" -b 1000 --title \"Crawl rate $hostname / $servicedesc\" ";
$def[4] =
  "DEF:crate=$RRDFILE[5]:$DS[5]:MAX ".
  "AREA:crate#ff8000:\"rate        \" ".
  "GPRINT:crate:LAST:\"%7.1lf %s last\" ".
  "GPRINT:crate:AVERAGE:\"%7.1lf %s avg\" ".
  "GPRINT:crate:MAX:\"%7.1lf %s max\\n\" ".
  "";

$ds_name[6] = 'Query rate';
$opt[5] = "--vertical-label \"queries/min\" -b 1000 --title \"Queries per minute $hostname / $servicedesc\" ";
$def[5] =
  "DEF:qrate=$RRDFILE[6]:$DS[6]:MAX ".
  "AREA:qrate#00ffc0:\"rate        \" ".
  "GPRINT:qrate:LAST:\"%7.1lf %s last\" ".
  "GPRINT:qrate:AVERAGE:\"%7.1lf %s avg\" ".
  "GPRINT:qrate:MAX:\"%7.1lf %s max\\n\" ".
  "";

?>
