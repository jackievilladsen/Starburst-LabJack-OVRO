#!/usr/bin/env python

# Created 2 May 2016 by Jackie Villadsen
# starburst_select.py
#
# Purpose: Set LO frequency and RF/noise switch for Starburst.  Prints DCM power after settings applied.
# Usage: ./starburst_select.py [input] [band #]
# Examples:
#    ./starburst_select.py RF 1
#          Selects RF input to DCMs, sets LO frequency to 3.4 GHz.
#    ./starburst_select noise 2
#          Selects noise (or signal generator) input to DCMs, sets LO frequency to 7.5 GHz.
# Input options: RF, noise
# Band # options: 1, 2, 3, 4 --> LO freq is 3.4 GHz, 7.5 GHz, 11.5 GHz, 15.5 GHz
#
# Your python path must include the sblj module, found in /scr/jrv/labjacks

verbose = False # change this to True if you want the script to print all monitor data

import sys
try:
    from sblj import *    # sblj is the module with commands to run 
except:
    sys.exit('sblj module failed to import. Add \'/scr/jrv/labjacks\' to your python path.')

band_dict = {'1':LOFreqConstants.LO_3_4GHZ,
             '2':LOFreqConstants.LO_7_5GHZ,
             '3':LOFreqConstants.LO_11_5GHZ,
             '4':LOFreqConstants.LO_15_5GHZ}

# verify that the program was run with valid arguments
def check_args(switch,band):
    good_args = switch in ['RF','NOISE'] and band in band_dict.keys()
    return good_args
good_args = False
if len(sys.argv)>2:
    switch = sys.argv[1].upper()
    band = sys.argv[2]
    good_args = check_args(switch,band)
if not good_args:
    sys.exit('Bad arguments.  See top of starburst_select.py for instructions on command line arguments.')

print 'switch:', switch
print 'band:', band

# connect to Labjacks
try:
    lo = LONoiseLJ('LONM')
except:
    sys.exit('Connection to LONM labjack unsuccessful, quitting program without changing bands or switch.')
try:
    dcmA = AntennaLJ('DCMA')
except:
    sys.exit('Connection to DCMA labjack unsuccessful, quitting program without changing bands or switch.')

# set RF/noise switch
if switch=='RF':
    dcmA.selectRFSource()
elif switch=='NOISE':
    dcmA.selectNoiseSource()

# set LO frequency
lo.setLOFreq(band_dict[band])

# print DCM power neatly
print 'Readings from DCM power monitor (9.4 dBm has already been added to account for coupler): '
channels = ['HIPOW','HQPOW','VIPOW','VQPOW']
pow_dict = dcmA.getParams(channels)
for c in channels:
    print c + ':', pow_dict[c], 'dBm'

if verbose:
    # print all LO and DCM monitor data
    print '\nAll LO monitor data: ', lo.getParams()
    print '\nAll DCM A monitor data: ', dcmA.getParams()

print ' '

# disconnect from Labjacks
lo.disconnect()
dcmA.disconnect()
