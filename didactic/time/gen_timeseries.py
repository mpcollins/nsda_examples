#
#
# gen_timeseries.py
#
# Generates a timeseries output by reading flow records and partitioning 
# the data in this case, into short (<=4 packet) TCP flows, and long 
# (>4 packet) TCP flows. 
#
# Output
# Time <bytes> <packets> <addresses> <long bytes> <long packets> <long addresses>
#
# Takes as input
# rwcut --fields=sip,dip,bytes,packets,stime --epoch-time --no-title
#
# We assume that the records are chronologically ordered, that is, no record
# will produce an stime earlier than the records preceding it in the 
# output.

import sys 
current_time = sys.maxint
start_time = sys.maxint
bin_size = 300 # We'll use five minute bins for convenience
ip_set_long = set()
ip_set_short = set()
byte_count_long = 0 
byte_count_short = 0 
packet_count_long = 0 
packet_count_short = 0 
for i in sys.stdin.readlines(): 
    sip, dip, bytes, packets, stime = i[:-1].split('|')[0:5]
    # convert the non integer values
    bytes, packets, stime = map(lambda x: int(float(x)), (bytes, packets, stime))
    # Now we check the time binning; if we're onto a new bin, dump and 
    # reset the contents
    if (stime < current_time) or (stime > current_time + bin_size):
        ip_set_long = set()
        ip_set_short = set()
        byte_count_long = byte_count_short = 0 
	packet_count_long = packet_count_short = 0 
        if (current_time == sys.maxint): 
            # Set the time to a 5 minute period at the start of the
            # currently observed epoch.  This is done in order to 
            # ensure that the time values are always some multiple
            # of five minutes apart, as opposed to dumping something
            # at t, t+307, t+619 and so on.
            current_time = stime - (stime % bin_size) 
        else:
            # Now we output results
            print "%10d %10d %10d %10d %10d %10d %10d" % (
                current_time, len(ip_set_short), byte_count_short, 
                packet_count_short,len(ip_set_long), byte_count_long,
                packet_count_long)
            current_time = stime - (stime % bin_size) 
    else:
        # Instead of printing, we're just adding up data
        # First, determine if the flow is long or short
        if (packets <= 4): 
            # flow is short
            byte_count_short += bytes
            packet_count_short += packets
            ip_set_short.update([sip,dip])
        else:
            byte_count_long += bytes
            packet_count_long += packets
            ip_set_long.update([sip,dip])

if byte_count_long + byte_count_short != 0:
    # Final print line check
    print "%10d %10d %10d %10d %10d %10d %10d" % (
    	  	     	  current_time, len(ip_set_short), byte_count_short, 
			  packet_count_short,len(ip_set_long), byte_count_long,
                          packet_count_long)
            
