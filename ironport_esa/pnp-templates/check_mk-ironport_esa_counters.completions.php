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

$opt[1] = "--vertical-label 'Completed per sec' -l0 --title \"IronPort Completed Recipients for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:total=".$RRD['Total']." " ;
$def[1] .= "LINE:total#F51D30:\"Total             \" " ;
$def[1] .= "GPRINT:total:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:total:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:total:MAX:\"Max\: %6.2lf/s\\n\" " ;
$def[1] .= "COMMENT:\" \\n\" ";

$def[1] .= "DEF:deleted=".$RRD['Deleted']." " ;
$def[1] .= "LINE:deleted#8F9286:\"Deleted           \" " ;
$def[1] .= "GPRINT:deleted:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:deleted:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:deleted:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:unsub=".$RRD['Global_Unsub_Hits']." " ;
$def[1] .= "LINE:unsub#00A348:\"Global Unsub Hits \" " ;
$def[1] .= "GPRINT:unsub:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:unsub:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:unsub:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:delivered=".$RRD['Delivered']." " ;
$def[1] .= "LINE:delivered#FFFF00:\"Delivered         \" " ;
$def[1] .= "GPRINT:delivered:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:delivered:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:delivered:MAX:\"Max\: %6.2lf/s\\n\" " ;

?>
