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

$opt[1] = "--vertical-label 'conn. @ query time' -l0 --title \"IronPort Connections for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:in=".$RRD['Connections_In']." " ;
$def[1] .= "LINE:in#F51D30:\"Incoming        \" " ;
$def[1] .= "GPRINT:in:LAST:\"Current\: %8.2lf\" " ;
$def[1] .= "GPRINT:in:AVERAGE:\"Average\: %8.2lf\" " ;
$def[1] .= "GPRINT:in:MAX:\"Max\: %8.2lf\\n\" " ;

$def[1] .= "DEF:out=".$RRD['Connections_Out']." " ;
$def[1] .= "LINE:out#8F9286:\"Outgoing        \" " ;
$def[1] .= "GPRINT:out:LAST:\"Current\: %8.2lf\" " ;
$def[1] .= "GPRINT:out:AVERAGE:\"Average\: %8.2lf\" " ;
$def[1] .= "GPRINT:out:MAX:\"Max\: %8.2lf\\n\" " ;

$opt[2] = "--vertical-label 'active messages' -l0 --title \"IronPort Active Messages for $hostname\" ";

$def[2] = "";

$def[2] .= "DEF:wqueue=".$RRD['Messages_in_Work_queue']." " ;
$def[2] .= "LINE:wqueue#F51D30:\"in Work Queue   \" " ;
$def[2] .= "GPRINT:wqueue:LAST:\"Current\: %8.2lf\" " ;
$def[2] .= "GPRINT:wqueue:AVERAGE:\"Average\: %8.2lf\" " ;
$def[2] .= "GPRINT:wqueue:MAX:\"Max\: %8.2lf\\n\" " ;

$def[2] .= "DEF:quarantine=".$RRD['Messages_in_Quarantine']." " ;
$def[2] .= "LINE:quarantine#8F9286:\"in Quarantine   \" " ;
$def[2] .= "GPRINT:quarantine:LAST:\"Current\: %8.2lf\" " ;
$def[2] .= "GPRINT:quarantine:AVERAGE:\"Average\: %8.2lf\" " ;
$def[2] .= "GPRINT:quarantine:MAX:\"Max\: %8.2lf\\n\" " ;

$opt[3] = "--vertical-label 'active objects' -l0 --title \"IronPort Destination Objects for $hostname\" ";

$def[3] = "";

$def[3] .= "DEF:objects=".$RRD['Destination_Objects_in_Memory']." " ;
$def[3] .= "LINE:objects#F51D30:\"Objects in memory\" " ;
$def[3] .= "GPRINT:objects:LAST:\"Current\: %8.2lf\" " ;
$def[3] .= "GPRINT:objects:AVERAGE:\"Average\: %8.2lf\" " ;
$def[3] .= "GPRINT:objects:MAX:\"Max\: %8.2lf\\n\" " ;

?>
