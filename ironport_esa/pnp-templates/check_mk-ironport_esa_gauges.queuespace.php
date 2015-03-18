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

$opt[1] = "--vertical-label 'Byte' -l0 --title \"IronPort Queue Space for $hostname\" ";

$def[1] = "";

$def[1] .= "DEF:freekb=".$RRD['Total_Free']." " ;
$def[1] .= "CDEF:free=freekb,1024,* ";

$def[1] .= "DEF:usedkb=".$RRD['Total_Used']." " ;
$def[1] .= "CDEF:used=usedkb,1024,* ";

$def[1] .= "CDEF:size=free,used,+ ";
$def[1] .= "COMMENT:\"Size\:                         \" ";
$def[1] .= "GPRINT:size:LAST:\"%6.2lf %sB\\n\" ";
$def[1] .= "COMMENT:\" \\n\" ";

$def[1] .= "LINE:used#F51D30:\"Total Used         \" " ;
$def[1] .= "GPRINT:used:LAST:\"Current\: %6.2lf %sB\" " ;
$def[1] .= "GPRINT:used:AVERAGE:\"Average\: %6.2lf %sB\" " ;
$def[1] .= "GPRINT:used:MAX:\"Max\: %6.2lf %sB\\n\" " ;

$def[1] .= "DEF:quarantinekb=".$RRD['Used_by_Quarantine']." " ;
$def[1] .= "CDEF:quarantine=quarantinekb,1024,* ";
$def[1] .= "LINE:quarantine#8F9286:\"Used by Quarantine \" " ;
$def[1] .= "GPRINT:quarantine:LAST:\"Current\: %6.2lf %sB\" " ;
$def[1] .= "GPRINT:quarantine:AVERAGE:\"Average\: %6.2lf %sB\" " ;
$def[1] .= "GPRINT:quarantine:MAX:\"Max\: %6.2lf %sB\\n\" " ;
$def[1] .= "COMMENT:\" \\n\" ";

$def[1] .= "CDEF:util=used,100,*,size,/ ";
$def[1] .= "COMMENT:\"Utilization\:         \" ";
$def[1] .= "GPRINT:util:LAST:\"Current\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:util:AVERAGE:\" Average\: %6.2lf %%\" " ;
$def[1] .= "GPRINT:util:MAX:\" Max\: %6.2lf%%\\n\" " ;

?>
