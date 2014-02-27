#/usr/bin/env python
#
#
# centrality.py
#
# script which generates centrality statistics for a dataset
#
# input:
# A table of pairs in the form source, destination with a space separating them
# Weight is implicit, the weight of a link is the number of times a pair appears
#
# command_line
# calc_centrality.py n
# n: integer value, the number of elements to return in the report
#
# Output
# 7 Column report of the form rank | betweenness winner | betweenness
# score | degree winner | degree score | closeness winner | closeness
# score
import sys,string
import apsp

n = int(sys.argv[1])

closeness_results = []
degree_results = []
betweenness_results = []

target_graph = apsp.WeightedGraph() 

# load up the graph
for i in sys.stdin.readlines():
    source, dest = i[:-1].split()
    target_graph.add_link(source, dest, 1)

# Calculate degree centrality; the easiest of the bunch since it's just the
# degree
for i in target_graph.nodes:
    degree_results.append((i, len(target_graph.neighbors(i))))

apsp_results = target_graph.apsp()

# Now, calculate the closeness centrality scores
for i in target_graph.nodes:
    dt = apsp_results[i][0] # This is the distance table
    total_distance = reduce(lambda a,b:a+b, dt.values())
    closeness_results.append((i, total_distance))

# Now, we calcualte betweenness centrality scores

bt_table = {}
for i in target_graph.nodes:
    bt_table[i] = 0

for current_node in target_graph.nodes:
    # Reconstruct the shortest paths from the predecessor table; 
    # for every entry in the distance table, walk backwards from that 
    # entry to the correspending origin to get the shortest path, then
    # count the nodes in that path on the master bt table
    pred_table = apsp_results[i][1] # We have the predecessor table
    sp_list = apsp_results[i][0]
    if current_node in sp_list.keys():
        path = []
        for working_node in sp_list.keys(): 
            if working_node != current_node:
                # We should be done with working node at this point, count
                # the nodes there for bt score
                for i in path:
                    bt_table[i] += 1
            else:
                path.append(working_node)
                working_node = pred_table[working_node]

for i in bt_table.keys():
    betweenness_results.append((i,bt_table[i]))

# Order the tables, remember that betweenness and degree use higher score, closeness
# lower score

degree_results.sort(lambda a,b:b[1]-a[1])
betweenness_results.sort(lambda a,b:b[1]-a[1])
closeness_results.sort(lambda a,b:a[1]-b[1])

print "%5s|%15s|%10s|%15s|%10s|%15s|%10s" % ("Rank", "Between", "Score", "Degree", "Score","Close", "Score")
for i in range(0, n):
    print "%5d|%15s|%10d|%15s|%10d|%15s|%10d" % ( i + 1,
                                                  str(betweenness_results[i][0]),
                                                  betweenness_results[i][1],
                                                  str(degree_results[i][0]),
                                                  degree_results[i][1],
                                                  str(closeness_results[i][0]),
                                                  closeness_results[i][1])



 
