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

setlocale(LC_ALL, "POSIX");

// Make data sources available via names
$RRD = array();
foreach ($NAME as $i => $n) {
    $RRD[$n]     = "$RRDFILE[$i]:$DS[$i]:MAX";
    $RRD_MIN[$n] = "$RRDFILE[$i]:$DS[$i]:MIN";
    $RRD_AVG[$n] = "$RRDFILE[$i]:$DS[$i]:AVERAGE";
    $WARN[$n] = $WARN[$i];
    $CRIT[$n] = $CRIT[$i];
    $MIN[$n]  = $MIN[$i];
    $MAX[$n]  = $MAX[$i];
}

$opt[1] = "--vertical-label 'Utilization %' -l0 --title \"IronPort General Resource Utilization for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:ram=".$RRD['Memory_utilization']." " ;
$def[1] .= "LINE:ram#F51D30:\"Memory                \" " ;
$def[1] .= "GPRINT:ram:LAST:\"Current\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:ram:AVERAGE:\"Average\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:ram:MAX:\"Max\: %6.2lf %%\\n\" " ;

$def[1] .= "DEF:diskio=".$RRD['Disk_utilization']." " ;
$def[1] .= "LINE:diskio#8F9286:\"Disk I/O              \" " ;
$def[1] .= "GPRINT:diskio:LAST:\"Current\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:diskio:AVERAGE:\"Average\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:diskio:MAX:\"Max\: %6.2lf %%\\n\" " ;

$def[1] .= "DEF:conservation=".$RRD['Resource_conservation']." " ;
$def[1] .= "LINE:conservation#0000FF:\"Resource Conservation \" " ;
$def[1] .= "GPRINT:conservation:LAST:\"Current\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:conservation:AVERAGE:\"Average\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:conservation:MAX:\"Max\: %6.2lf %%\\n\" " ;

?>
