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

$opt[1] = "--vertical-label 'per sec' -l0 --title \"IronPort DNS Status for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:dns=".$RRD['DNS_Requests']." " ;
$def[1] .= "LINE:dns#F51D30:\"DNS Requests     \" " ;
$def[1] .= "GPRINT:dns:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:dns:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:dns:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:network=".$RRD['Network_Requests']." " ;
$def[1] .= "LINE:network#8F9286:\"Network Requests \" " ;
$def[1] .= "GPRINT:network:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:network:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:network:MAX:\"Max\: %6.2lf/s\\n\" " ;
$def[1] .= "COMMENT:\" \\n\" ";

$def[1] .= "DEF:hits=".$RRD['Cache_Hits']." " ;
$def[1] .= "LINE:hits#00A348:\"Cache Hits       \" " ;
$def[1] .= "GPRINT:hits:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:hits:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:hits:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:misses=".$RRD['Cache_Misses']." " ;
$def[1] .= "LINE:misses#FFFF00:\"Cache Misses     \" " ;
$def[1] .= "GPRINT:misses:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:misses:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:misses:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:exceptions=".$RRD['Cache_Exceptions']." " ;
$def[1] .= "LINE:exceptions#002A97:\"Cache Exceptions \" " ;
$def[1] .= "GPRINT:exceptions:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:exceptions:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:exceptions:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:expired=".$RRD['Cache_Expired']." " ;
$def[1] .= "LINE:expired#000000:\"Cache Expired    \" " ;
$def[1] .= "GPRINT:expired:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:expired:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:expired:MAX:\"Max\: %6.2lf/s\\n\" " ;

?>
