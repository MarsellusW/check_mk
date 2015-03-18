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

$opt[1] = "--vertical-label 'CPU utilization %' -l0  -u 100 --title \"CPU Utilization for $hostname\" ";
#
$def[1] =  "DEF:utila=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .=  "DEF:utilc=$RRDFILE[2]:$DS[2]:AVERAGE " ;
$def[1] .=  "DEF:utild=$RRDFILE[3]:$DS[3]:AVERAGE " ;

$def[1] .= "LINE:utilc#F51D30FF:\"Control CPU    \" " ;
$def[1] .= "GPRINT:utilc:LAST:\"%6.1lf%% last\" " ;
$def[1] .= "GPRINT:utilc:AVERAGE:\"%6.1lf%% avg\" " ;
$def[1] .= "GPRINT:utilc:MIN:\"%6.1lf%% min\" " ;
$def[1] .= "GPRINT:utilc:MAX:\"%6.1lf%% max\\n\" " ;

$def[1] .= "LINE:utild#00A348FF:\"Data CPU       \" " ;
$def[1] .= "GPRINT:utild:LAST:\"%6.1lf%% last\" " ;
$def[1] .= "GPRINT:utild:AVERAGE:\"%6.1lf%% avg\" " ;
$def[1] .= "GPRINT:utild:MIN:\"%6.1lf%% min\" " ;
$def[1] .= "GPRINT:utild:MAX:\"%6.1lf%% max\\n\" " ;

$def[1] .= "LINE:utila#002A97FF:\"Average CPU    \" " ;
$def[1] .= "GPRINT:utila:LAST:\"%6.1lf%% last\" " ;
$def[1] .= "GPRINT:utila:AVERAGE:\"%6.1lf%% avg\" " ;
$def[1] .= "GPRINT:utila:MIN:\"%6.1lf%% min\" " ;
$def[1] .= "GPRINT:utila:MAX:\"%6.1lf%% max\\n\" " ;

?>
