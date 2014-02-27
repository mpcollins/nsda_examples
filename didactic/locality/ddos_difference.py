#!/usr/bin/env python
#
# ddos_intersection.py
#
# input:
#       Nothing
# output:
#       A report comparing the number of addresses in two sets, ordered by the
#       largest number of hosts in set A which are not present in set B.
#
#  command_line
#  ddos_intersection.py historical_set ddos_set 
#
#  historical_set: a set of historical data giving external addresses
#  which have historically spoken to a particular host or network
#  ddos_set: a set of data from a ddos attack on the host
#  This is going to work off of /24's for simplicity. 
#
import sys,os,tempfile

historical_setfn = sys.argv[1]
ddos_setfn = sys.argv[2]
blocksize = int(sys.argv[3])

mask_fh, mask_fn = tempfile.mkstemp()
os.close(mask_fh)
os.unlink(mask_fn)

# Create a netmask set off the historical set, we'll use this for intersection purposes
os.system("rwsettool --mask=24 --output-path=stdout %s | rwsetcat | sed 's/$/\/24/' | rwsetbuild stdin %s" % (historical_setfn, mask_fn))

bins = {}
# Read and store all the /24's in the historical data
a = os.popen('rwsettool --intersect %s %s --output-path=stdout | rwsetcat --network-structure=C' % (mask_fn, historical_setfn),'r')
for i in a.readlines():
    address, count = i[:-1].split('|')[0:2]
    bins[address] = [int(count), 0] # First column is historical, second column is ddos
a.close()
# Repeat the process with all the data in the ddos set
a = os.popen('rwsettool --intersect %s %s --output-path=stdout | rwsetcat --network-structure=C' % (mask_fn, ddos_setfn),'r')
for i in a.readlines():
    address, count = i[:-1].split('|')[0:2]
    # I'm intersecting the maskfile again, since I originally intersected it against the
    # file I generated the maskfile from, any address that I find in the file will
    # already be in the bins associative array
    bins[address][1] = int(count)

#
# Now we order the contents of the bins.  This script is implicitly written to support a
# whitelist-based approach -- addresses which appear in the historical data are candidates
# for whitelisting, all other addresses will be blocked.  We order the candidate
# blocks in terms of the number of historical addresses allowed in, decreasing
# for every attacker address allowed in.
address_list = bins.items()
address_list.sort(lambda x,y:(y[1][0]-x[1][0])-(y[1][1]-x[1][1]))
print "%20s|%10s|%10s" % ("Block", "Not-DDoS", "DDoS")
for address, result in address_list:
    print "%20s|%10d|%10d" % (address, bins[address][0], bins[address][1])
    
