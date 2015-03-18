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

$opt[1] = "--vertical-label 'Recipients' -l0 --title \"IronPort Active Recipients for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:total=".$RRD['Total_Active']." " ;
$def[1] .= "LINE:total#F51D30:\"Total        \" " ;
$def[1] .= "GPRINT:total:LAST:\"Current\: %8.2lf\" " ;
$def[1] .= "GPRINT:total:AVERAGE:\"Average\: %8.2lf\" " ;
$def[1] .= "GPRINT:total:MAX:\"Max\: %8.2lf\\n\" " ;
$def[1] .= "COMMENT:\" \\n\" ";

$def[1] .= "DEF:attempted=".$RRD['Attempted']." " ;
$def[1] .= "LINE:attempted#8F9286:\"Attempted    \" " ;
$def[1] .= "GPRINT:attempted:LAST:\"Current\: %8.2lf\" " ;
$def[1] .= "GPRINT:attempted:AVERAGE:\"Average\: %8.2lf\" " ;
$def[1] .= "GPRINT:attempted:MAX:\"Max\: %8.2lf\\n\" " ;

$def[1] .= "DEF:unattempted=".$RRD['Unattempted']." " ;
$def[1] .= "LINE:unattempted#0000FF:\"Unattempted  \" " ;
$def[1] .= "GPRINT:unattempted:LAST:\"Current\: %8.2lf\" " ;
$def[1] .= "GPRINT:unattempted:AVERAGE:\"Average\: %8.2lf\" " ;
$def[1] .= "GPRINT:unattempted:MAX:\"Max\: %8.2lf\\n\" " ;

?>
