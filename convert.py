#subproperty of
# this file tests if there is any cycle in the subpropertyof graph.


from hdt import HDTDocument, IdentifierPosition
import pandas as pd
import numpy as np
import datetime
import pickle
import time
import networkx as nx
import sys
import csv
# from z3 import *
from bidict import bidict
import matplotlib.pyplot as plt
import tldextract
import json
import random
from equiClass import equiClassManager
# import random
# from rdflib import Graph
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
# from sets import Set
PATH_LOD = "./LOD-a-lot/refined-subC-FA.hdt"
PATH_EQ = "./sameAs/term2id_0-99.csv"




class SubM:

    # Initializer / Instance Attributes
    def __init__(self, path_hdt = PATH_LOD, path_eq = PATH_EQ):
        self.hdt = HDTDocument(path_hdt)

        self.subClassOf = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
        self.id_subClassOf = self.hdt.convert_term("http://www.w3.org/2000/01/rdf-schema#subClassOf", IdentifierPosition.Predicate)

        self.equivalent = "http://www.w3.org/2002/07/owl#equivalentClass"
        self.id_equivalentClass = self.hdt.convert_term("http://www.w3.org/2002/07/owl#equivalentClass", IdentifierPosition.Predicate)

        self.subPropertyOf = "http://www.w3.org/2000/01/rdf-schema#subPropertyOf"
        self.id_subPropertyOf = self.hdt.convert_term("http://www.w3.org/2000/01/rdf-schema#subPropertyOf", IdentifierPosition.Predicate)

# owl:equivalentProperty

        self.equivalentProperty = "http://www.w3.org/2002/07/owl#equivalentProperty"
        self.id_equivalentProperty = self.hdt.convert_term("http://www.w3.org/2002/07/owl#equivalentProperty", IdentifierPosition.Predicate)


        self.graph = nx.DiGraph()

        self.sameAs = None
        self.term2id = None
        self.edge2id = None


        print ('set up the equivalence class manager')
        # self.diagnosed_relations = [] # the result
        # self.suggestion_on_relations = [] # from the manual decison and Joe's sameAs data. Triple
        # self.leaf_classes = set()

        print ('finished initialization')

    def setup_graph(self):

        self.sameAs = equiClassManager(PATH_EQ)
        self.term2id = set()
        self.edge2id = set()

        print('set up the graph')
        (subclass_triples, cardinality) = self.hdt.search_triples("", self.subClassOf , "")

        coll_gid = set()
        coll_id = set()
        collect_pairs = []

        count_L = 0
        count_R = 0
        count_LR = 0
        count_N = 0

        for (s, _, o) in subclass_triples:
            s_id = self.hdt.convert_term(s, IdentifierPosition.Subject)
            o_id = self.hdt.convert_term(o, IdentifierPosition.Object)
            s_gid = self.sameAs.find_index(s)
            o_gid = self.sameAs.find_index(o)
            # four cases
            if s_gid == None and o_gid == None:
                collect_pairs.append((s_id, o_id))
                coll_id.add(s_id)
                coll_id.add(o_id)
                self.term2id.add((s, s_id, 0, s_id))
                self.term2id.add((o, o_id, 0, o_id))
                self.edge2id.add((s_id, o_id, s, o))
                count_N += 1
            elif s_gid != None and o_gid == None:
                collect_pairs.append((s_gid, o_id))
                coll_gid.add(s_gid)
                coll_id.add(s_id)
                self.term2id.add((s, s_id, s_gid, s_gid))
                self.term2id.add((o, o_id, 0, o_id))
                self.edge2id.add((s_gid, o_id, s, o))
                count_L += 1
            elif s_gid == None and o_gid != None:
                collect_pairs.append((s_id, o_gid))
                coll_gid.add(o_gid)
                coll_id.add(s_id)
                self.term2id.add((s, s_id, 0, s_id))
                self.term2id.add((o, o_id, o_gid, o_gid))
                self.edge2id.add((s_id, o_gid, s, o))
                count_R += 1
            elif s_gid != None and o_gid != None:
                collect_pairs.append((s_gid, o_gid))
                coll_gid.add(s_gid)
                coll_gid.add(o_gid)
                self.term2id.add((s, s_id, s_gid, s_gid))
                self.term2id.add((o, o_id, o_gid, o_gid))
                self.edge2id.add((s_gid, o_gid, s, o))
                count_LR += 1

        print ('L = ', count_L)
        print ('R = ', count_R)
        print ('LR = ', count_LR)
        print ('Neither = ', count_N)

        it = coll_gid & coll_id
        print ('test if there is any id overlapping', len(it))

        print ('there are ', len (collect_pairs), 'edges')
        print ('among them, there are ', len (coll_gid), ' nodes are mapped to the sameas group ids')
        self.graph.add_edges_from(collect_pairs)


    def convert_to_id(self, term):
        if term == "akt742:Intangible-Thing":
            # this is the only class that has two different ids (as subject and object)
            return 2601100675
        else:
            return self.hdt.convert_term(term, IdentifierPosition.Subject)

    def convert_to_term(self, id):
        if id == 2601100675:
            return "akt742:Intangible-Thing"
            # this is the only one that has two different ids (as subject and object)
        else:
            return self.hdt.convert_id(id, IdentifierPosition.Subject)



    def test_cycle(self):
        try:
            c = nx.find_cycle(self.graph) # change to simple_cycles ??
            print ('cycle = ', c)

        except Exception as e:
            # hint_not_working = True
            print ('no cycle')

    def export_graph(self, name):

        file =  open(name, 'w', newline='')
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_ID", "OBJECT_ID"])

        for (s_id, o_id) in self.graph.edges:
            writer.writerow([s_id, o_id])


        g.serialize(destination=name, format='nt')

    def export_term2id(self, name):
        file =  open(name, 'w', newline='')
        writer = csv.writer(file)
        writer.writerow([ "TERM","ID","GROUPID", "NEWID"])

        for (term, id, gid, new_id) in self.term2id:
            writer.writerow([term, id, gid, new_id])


    def export_edge2id(self, name):
        file =  open(name, 'w', newline='')
        writer = csv.writer(file)
        writer.writerow([ "SUBJECT_NEWID","OBJECT_NEWID","SUBJECT", "OBJECT"])

        for (s_nid, o_nid, s, o) in self.edge2id:
            writer.writerow([s_nid, o_nid, s, o])



def main ():
    print ('start')
    start = time.time()
    # ==============
    # some small tests
    sm = SubM()

    sm.setup_graph()
    # sp.export_graph_nt('subC-all.nt')


    sm.export_graph('mapped_graph_edges.csv')
    sm.export_term2id('node_mapping.csv')
    sm.export_edge2id('edge_mapping.csv')

    # sm.test_cycle()
    # sp.export_graph_nt('refined-subC-SA.nt')
    # ===============
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Time taken: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))



if __name__ == "__main__":
    main()
