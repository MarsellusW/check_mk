<?php

# Palo Alto Sessions Counters - Spread over 3 files
$opt[1] = " --vertical-label \"sessions\" --title \"$hostname / $servicedesc\" ";
$def[1] = "DEF:var1=$RRDFILE[3]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var2=$RRDFILE[4]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var3=$RRDFILE[5]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var4=$RRDFILE[6]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var5=$RRDFILE[7]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var6=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:var7=$RRDFILE[2]:$DS[1]:AVERAGE " ;
$def[1] .= "AREA:var1#FF0000:\"total          \" " ;
$def[1] .= "GPRINT:var1:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var1:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var1:MAX:\"%7.0lf max\\n\" " ;
$def[1] .= "AREA:var2#FF8800:\"tcp            \" " ;
$def[1] .= "GPRINT:var2:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var2:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var2:MAX:\"%7.0lf max\\n\" " ;
$def[1] .= "STACK:var3#BFFF00:\"udp            \" " ;
$def[1] .= "GPRINT:var3:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var3:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var3:MAX:\"%7.0lf max\\n\" " ;
$def[1] .= "STACK:var4#8D85F3:\"icmp           \" " ;
$def[1] .= "GPRINT:var4:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var4:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var4:MAX:\"%7.0lf max\\n\" " ;
$def[1] .= "STACK:var5#FF897C:\"ssl proxy      \" " ;
$def[1] .= "GPRINT:var5:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var5:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var5:MAX:\"%7.0lf max\\n\" " ;
$def[1] .= "AREA:var6#FFFFFF00:\"% Utilization  \" " ;
$def[1] .= "GPRINT:var6:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var6:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var6:MAX:\"%7.0lf max\\n\" " ;
$def[1] .= "COMMENT:\"              \\n\" " ;
$def[1] .= "COMMENT:\"max allowed      \" " ;
$def[1] .= "GPRINT:var7:LAST:\"%7.0lf last\" " ;
$def[1] .= "GPRINT:var7:AVERAGE:\"%7.0lf avg\" " ;
$def[1] .= "GPRINT:var7:MAX:\"%7.0lf max\\n\" " ;

?>
