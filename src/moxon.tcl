#!/usr/bin/env	wish
#
#
#Copyright (C) 2014 Jim Richardson 
#email	weaselkeeper@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
#	02111-1307, USA.
#
#This program is a simple calculator for some basic parabolic
#antenna equations. It's crude, but at least seems bug free. It
#makes a few assumptions, first that the numbers are all related
#to free space, so any atmospheric losses, including rain fade
#must be calculated seperately (I may add this at a future time)
#Second, it assumes that you know not to use dumb combinations of
#numbers, like a parabolic dish of 10cm, with a freq of 100Mhz.
#The numbers generated in such a combo are mathematically
#correct, and in practical terms, bogus.
#I also assume that both antennas are the same diameter, this
#will change in future revisions.
#
#Most of the calculations come from a GTE microwave journal
#that is over 30 years old :) Information is forever.
#
#Comments, bug notices, feature lists are welcome at 
#weaselkeeper@gmail.com, please direct flames to /dev/null, I will...



set VERSION 0.01

wm title  . "Moxon calculator. $VERSION"
. config -bd 2


#set upper and lower limits for freq, path length etc
#

set freq 0.1	;#100 MHz

set wiredia 4	;# in mm

#frame for sliders

frame .main -width 400 -height 200 -bd 10
label .main.welcome -text "Welcome"
scale .main.dia -orient horiz -from 0 -to 50 \
	-resolution .5 -variable $wiredia \
	-label "wire diameter (mm) " -command {change_dia}
scale .main.freq -orient horiz -from 0 -to 500 \
	-resolution .25 -variable $freq \
	-label "Frequency (MHz)" -command {change_freq}
button .main.quit -text "quit" -command exit

pack .main
foreach widgets  {dia freq quit} {
pack .main.$widgets -side top
}

#Calculations begin here
#

#######################################33
# Slider changes cause stuff to happen
proc change_dia {new_dia} {
	#recalc all the parameters that are affected by 
	#change in wire diameter
	
	global freq
	set wire_dia $new_dia
	}

proc change_freq {new_freq} {
	#Recalc all the paramaters which are affected by 
	#changes in the freq  eg all of them
	global freq
	set freq $new_freq
	}

