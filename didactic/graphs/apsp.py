#!/usr/bin/env python
# 
# apsp.py -- implemented weighted paths and dijkstra's algorithm

import sys,os,basic_graph

class WeightedGraph(basic_graph.UndirGraph):
    def add_link(self, node_source, node_dest, weight):
        # Weighted bidirectional link aid, note that
        # we keep the aa, but now instead of simply setting the value to
        # 1, we add the weight value.  This reverts to an unweighted
        # graph if we always use the same weight.
        self.add_node(node_source)
        self.add_node(node_dest)
        if not self.links.has_key(node_source):
            self.links[node_source] = {}
        if not self.links[node_source].has_key(node_dest):
            self.links[node_source][node_dest] = 0
        self.links[node_source][node_dest] += weight
        if not self.links.has_key(node_dest):
            self.links[node_dest] = {}
        if not self.links[node_dest].has_key(node_source):
            self.links[node_dest][node_source] = 0
        self.links[node_dest][node_source] += weight
        
    def dijkstra(self, node_source):
        # Given a source node, create a map of paths for each vertex
        D = {}  # Tentative distnace table
        P = {}  # predecessor table

        # The predecessor table exploits a unique feature of shortest paths,
        # every subpath of a shortest path is itself a shortest path, so if
        # you find that (B,C,D) is the shortest path from A to E, then
        # (B,C) is the shortest path from A to D.  All you have to do is keep
        # track of the predecessor and walk backwards.  
         
        infy = 999999999999  # Shorthand for infinite
        for i in self.nodes:
            D[i] = infy
            P[i] = None

        D[node_source] = 0
        node_list = list(self.nodes)
        while node_list != []:
            current_distance = infy
            current_node = None
            # Step 1, find the node with the smallest distance, that'll
            # be node_source in the first call as it's the only one
            # where D =0 
            for i in node_list:
                if D[i] < current_distance:
                    current_distance = D[i]
                    current_node = i
            node_index = node_list.index(i)
            del node_list[node_index] # Remove it from the list
            if current_distance == infy:
                break # We've exhausted all paths from the node,
                      # everything else is in a different component
            for i in self.neighbors(current_node):
                new_distance = D[current_node] + self.links[current_node][i]
                if new_distance < D[i]:
                    D[i] = new_distance
                    P[i] = current_node
                    node_list.insert(0, i)
        for i in D.keys():
            if D[i] == infy:
                del D[i]
        for i in P.keys():
            if P[i] is None:
                del P[i]
        return D,P

    def apsp(self):
        # Calls dijkstra repeatedly to create an all-pairs shortest paths table
        apsp_table = {}
        for i in self.nodes:
            apsp_table[i] = self.dijkstra(i)
        return apsp_table


    
