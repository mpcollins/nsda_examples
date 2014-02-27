#!/usr/bin/env python
#
# basic_graph.py
#
# Library
# Provides:
#         Graph Object, which as a constructor takes a flow file
#
import os, sys

class UndirGraph:
    """ An undirected, unweighted graph class. This also serves as the base class
    for all other graph implementations in this chapter """
    def add_node(self, node_id):
        self.nodes.add(node_id)

    def add_link(self, node_source, node_dest):
        self.add_node(node_source)
        self.add_node(node_dest)
        if not self.links.has_key(node_source):
            self.links[node_source] = {}
        self.links[node_source][node_dest] = 1
        if not self.links.has_key(node_dest):
            self.links[node_dest] = {}
        self.links[node_dest][node_source] = 1
        return
    
    def count_links(self):
        total = 0
        for i in self.links.keys():
            total += len(self.links[i].keys())
        return total/2 # Compensating for link doubling in undirected graph
        
    def neighbors(self, address):
        # Returns a list of all the nodes adjacent to the node address,
        # returns an empty list of there are no ndoes (technically impossible with
        # these construction rules, but hey).  
        if self.nodes.has_key(address):
            return self.links[address].keys()
        else:
            return None

    def __str__(self):
        return 'Undirected graph with %d nodes and %d links' % (len(self.nodes),
                                                                self.count_links())


    def adjacent(self, sip, dip):
        # Note, we've defined the graph as undirected during construction,
        # consequently links only has to return the source. 
        if self.links.has_key(sip):
            if self.links[sip].has_key(dip):
                return True
            
    def __init__(self):
        #
        # This graph is implemented using adjacency lists; every node has
        # a key in the links hashtable, and the resulting value is another hashtable.
        #
        # The nodes table is redundant for undirected graphs, since the existence of a
        # link between X and Y implies a link between Y and X, but in the case of
        # directed graphs it'll providea speedup if I'm just looking for a particular
        # node.
        self.links = {}
        self.nodes = set()
        
class DirGraph(UndirGraph):
    def add_link(self, node_source, node_dest):
        # Note that in comparison to the undirected graph, we only
        # add links in one direction
        self.add_node(node_source)
        self.add_node(node_dest)
        if not self.links.has_key(node_source):
            self.links[node_source] = {}
        self.links[node_source][node_dest] = 1
        return

    def count_links(self):
        # This had to be changed from the original count_links since I'm now
        # using an undirected graph.
        total = 0 
        for i in self.links.keys():
            total += len(self.links[i].keys())
        return total
            

if __name__ == '__main__':
    #
    # This is a stub executable that will create and then render an
    # undirected graph assuming that it receives some kind of
    # space delimited set of (source, dest) pairs on input
    #
    a = sys.stdin.readlines()
    tgt_graph = DirGraph()
    for i in a:
        source, dest = i.split()[0:2]
        tgt_graph.add_link(source, dest)
    print tgt_graph
    print "Links:"
    for i in tgt_graph.links.keys():
        dest_links = ' '.join(tgt_graph.links[i].keys())
        print '%s: %s' % (i, dest_links)


