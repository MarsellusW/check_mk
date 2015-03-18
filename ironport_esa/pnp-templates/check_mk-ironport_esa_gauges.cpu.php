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

#$opt[1] = "--slope-mode --vertical-label 'Utilization %' -l0 --title \"CPU Utilization for $hostname\" ";
$opt[1] = "--vertical-label 'Utilization %' -l0 --title \"CPU Utilization for $hostname\" ";

$def[1] = "";

if(isset($RRD['Total'])) {
    $def[1] .= "DEF:total=".$RRD_AVG['Total']." " ;
    $def[1] .= "LINE:total#F51D30:\"Total            \" " ;
    $def[1] .= "GPRINT:total:LAST:\"Last\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:total:AVERAGE:\"Avg\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:total:MAX:\"Max\: %6.1lf%%\\n\" " ;
    $def[1] .= "COMMENT:\" \\n\" ";
}
if(isset($RRD['Appliance'])) {
    $def[1] .= "DEF:appliance=".$RRD_AVG['Appliance']." " ;
    $def[1] .= "LINE:appliance#8F9286:\"Appliance        \" " ;
    $def[1] .= "GPRINT:appliance:LAST:\"Last\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:appliance:AVERAGE:\"Avg\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:appliance:MAX:\"Max\: %6.1lf%%\\n\" " ;
}
if(isset($RRD['Anti-Spam'])) {
    $def[1] .= "DEF:antispam=".$RRD_AVG['Anti-Spam']." " ;
    $def[1] .= "LINE:antispam#00A348:\"Anti-Spam        \" " ;
    $def[1] .= "GPRINT:antispam:LAST:\"Last\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:antispam:AVERAGE:\"Avg\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:antispam:MAX:\"Max\: %6.1lf%%\\n\" " ;
}
if(isset($RRD['Anti-Virus'])) {
    $def[1] .= "DEF:antivirus=".$RRD_AVG['Anti-Virus']." " ;
    $def[1] .= "LINE:antivirus#FFFF00:\"Anti-Virus       \" " ;
    $def[1] .= "GPRINT:antivirus:LAST:\"Last\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:antivirus:AVERAGE:\"Avg\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:antivirus:MAX:\"Max\: %6.1lf%%\\n\" " ;
}
if(isset($RRD['Reporting'])) {
    $def[1] .= "DEF:reporting=".$RRD_AVG['Reporting']." " ;
    $def[1] .= "LINE:reporting#002A97:\"Reporting        \" " ;
    $def[1] .= "GPRINT:reporting:LAST:\"Last\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:reporting:AVERAGE:\"Avg\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:reporting:MAX:\"Max\: %6.1lf%%\\n\" " ;
}
if(isset($RRD['Quarantine'])) {
    $def[1] .= "DEF:quarantine=".$RRD_AVG['Quarantine']." " ;
    $def[1] .= "LINE:quarantine#000000:\"Quarantine       \" " ;
    $def[1] .= "GPRINT:quarantine:LAST:\"Last\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:quarantine:AVERAGE:\"Avg\: %6.1lf%%\" " ;
    $def[1] .= "GPRINT:quarantine:MAX:\"Max\: %6.1lf%%\\n\" " ;
}

?>
