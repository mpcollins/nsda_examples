#!/usr/bin/env python
#
#
# compare_reports.py
#
# Command line: compare_reports.py file1 file2
#
# Reads the contents of two files and checks to see if the same 
# IP pairs appear.
#
import sys, os
def read_file(fn):
    ip_table = set()
    a = open(fn,'r')
    for i in a.readlines():
        sip, dip = map(lambda x:x.strip(), i.split('|')[0:2])
        key = "%15s:%15s" % (sip, dip)
        ip_table.add(key)
    a.close()
    return ip_table

if __name__ == '__main__':
    incoming = read_file(sys.argv[1])
    outgoing = read_file(sys.argv[2])
    missing_pairs = set()
    total_pairs = set()
    # Being a bit sloppy here, run on both incoming and outgoing to ensure
    # that if there's an element in one not in the other, it gets caught
    for i in incoming:
        total_pairs.add(i)
        if not i in outgoing:
            missing_pairs.add(i)
    for i in outgoing:
        total_pairs.add(i)
        if not i in incoming:
            missing_pairs.add(i)
    print missing_pairs, total_pairs
    # Now do some address breakdowns
    addrcount = {}
    for i in missing_pairs:
        in_value, out_value = i.split(':')[0:2]
        if not addrcount.has_key(in_value):
            addrcount[in_value] = 0
        if not addrcount.has_key(out_value):
            addrcount[out_value] = 0
        addrcount[in_value] += 1
        addrcount[out_value] += 1
    # Simple report, number of missing pairs, list of most commonly occurring
    # addresses
    print "%d missing pairs out of %d total" % (len(missing_pairs),
                                                len(total_pairs))
    s = addrcount.items()
    s.sort(lambda a,b:b[1] - a[1]) # lambda just guarantees order
    print "Most common addresses:"
    for i in s[0:10]:
        print "%15s %5d" % (i[0],addrcount[i[0]])
        
