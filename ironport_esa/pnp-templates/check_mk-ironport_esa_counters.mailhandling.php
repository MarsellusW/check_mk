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

$opt[1] = "--vertical-label 'Events per sec' -l0 --title \"IronPort Mail Handling Events for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:msgs=".$RRD['Messages_Received']." " ;
$def[1] .= "LINE:msgs#F51D30:\"Messages Received       \" " ;
$def[1] .= "GPRINT:msgs:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:msgs:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:msgs:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:recips=".$RRD['Recipients_Received']." " ;
$def[1] .= "LINE:recips#8F9286:\"Recipients Received     \" " ;
$def[1] .= "GPRINT:recips:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:recips:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:recips:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:bounce=".$RRD['Generated_Bounce_Recipients']." " ;
$def[1] .= "LINE:bounce#00A348:\"Gen. Bounce Recipients  \" " ;
$def[1] .= "GPRINT:bounce:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:bounce:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:bounce:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:rejected=".$RRD['Rejected_Recipients']." " ;
$def[1] .= "LINE:rejected#FFFF00:\"Rejected Recipients     \" " ;
$def[1] .= "GPRINT:rejected:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:rejected:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:rejected:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:dropped=".$RRD['Dropped_Messages']." " ;
$def[1] .= "LINE:dropped#002A97:\"Dropped Messages        \" " ;
$def[1] .= "GPRINT:dropped:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:dropped:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:dropped:MAX:\"Max\: %6.2lf/s\\n\" " ;

$def[1] .= "DEF:soft=".$RRD['Soft_Bounce_Events']." " ;
$def[1] .= "LINE:soft#000000:\"Soft Bounce Events      \" " ;
$def[1] .= "GPRINT:soft:LAST:\"Current\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:soft:AVERAGE:\"Average\: %6.2lf/s\" " ;
$def[1] .= "GPRINT:soft:MAX:\"Max\: %6.2lf/s\\n\" " ;

?>
