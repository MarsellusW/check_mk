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

$opt[1] = "--vertical-label 'Bounces per sec' -l0 --title \"IronPort Hard Bounced Recipients for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:total=".$RRD['Total']." " ;
$def[1] .= "LINE:total#F51D30:\"Total           \" " ;
$def[1] .= "GPRINT:total:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:total:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:total:MAX:\"Max\: %6.2lf/s\\n\" " ;
$def[1] .= "COMMENT:\" \\n\" ";

$def[1] .= "DEF:5xx=".$RRD['5XX']." " ;
$def[1] .= "LINE:5xx#8F9286:\"5XX             \" " ;
$def[1] .= "GPRINT:5xx:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:5xx:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:5xx:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:dns=".$RRD['DNS']." " ;
$def[1] .= "LINE:dns#00A348:\"DNS             \" " ;
$def[1] .= "GPRINT:dns:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:dns:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:dns:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:expired=".$RRD['Expired']." " ;
$def[1] .= "LINE:expired#FFFF00:\"Expired         \" " ;
$def[1] .= "GPRINT:expired:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:expired:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:expired:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:filter=".$RRD['Filter']." " ;
$def[1] .= "LINE:filter#002A97:\"Filter          \" " ;
$def[1] .= "GPRINT:filter:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:filter:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:filter:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:other=".$RRD['Other']." " ;
$def[1] .= "LINE:other#000000:\"Other           \" " ;
$def[1] .= "GPRINT:other:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:other:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:other:MAX:\"Max\: %6.2lf/s\\n\" " ;

?>
