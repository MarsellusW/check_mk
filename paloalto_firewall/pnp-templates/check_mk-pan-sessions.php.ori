<?php

# Palo Alto Sessions Counters - Spread over 3 files
$opt[1] = " --vertical-label \"sessions\" --title \"Sessions for $hostname / $servicedesc\" ";
$def[1] = "DEF:var1=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var2=$RRDFILE[2]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var3=$RRDFILE[3]:$DS[1]:AVERAGE " ;
$def[1] .= "AREA:var1#FF0000:\"active total\" " ;
$def[1] .= "GPRINT:var1:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var1:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var1:MAX:\"%7.0lf max\\n\" " ;
$def[1] .= "AREA:var2#FF8800:\"tcp active \" " ;
$def[1] .= "GPRINT:var2:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var2:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var2:MAX:\"%7.0lf max\\n\" ";
$def[1] .= "AREA:var3#BFFF00:\"udp active \" " ;
$def[1] .= "GPRINT:var3:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var3:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var3:MAX:\"%7.0lf max\\n\" ";

?>
