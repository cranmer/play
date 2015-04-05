/* -*- C++ -*-
 *
 * This file is a part of LEMON, a generic C++ optimization library
 *
 * Copyright (C) 2003-2008
 * Egervary Jeno Kombinatorikus Optimalizalasi Kutatocsoport
 * (Egervary Research Group on Combinatorial Optimization, EGRES).
 *
 * Permission to use, modify and distribute this software is granted
 * provided that this copyright notice appears in all copies. For
 * precise terms see the accompanying LICENSE file.
 *
 * This software is provided "AS IS" with no warranty of any kind,
 * express or implied, and with no claim as to its suitability for any
 * purpose.
 *
 */


#include <iostream>

#include <lemon/list_graph.h>
#include <lemon/dijkstra.h>

using namespace lemon;


int main (int, char*[])
{

    typedef ListGraph Graph;
    typedef Graph::Node Node;
    typedef Graph::Edge Edge;
    typedef Graph::EdgeMap<int> LengthMap;

    Graph g;

    //An example from Ahuja's book

    Node s=g.addNode();
    Node v2=g.addNode();
    Node v3=g.addNode();
    Node v4=g.addNode();
    Node v5=g.addNode();
    Node t=g.addNode();

    Edge s_v2=g.addEdge(s, v2);
    Edge s_v3=g.addEdge(s, v3);
    Edge v2_v4=g.addEdge(v2, v4);
    Edge v2_v5=g.addEdge(v2, v5);
    Edge v3_v5=g.addEdge(v3, v5);
    Edge v4_t=g.addEdge(v4, t);
    Edge v5_t=g.addEdge(v5, t);
  
    LengthMap len(g);

    len.set(s_v2, 10);
    len.set(s_v3, 10);
    len.set(v2_v4, 5);
    len.set(v2_v5, 8);
    len.set(v3_v5, 5);
    len.set(v4_t, 8);
    len.set(v5_t, 8);

    std::cout << "This program is a simple demo of the LEMON Dijkstra class."
              << std::endl;
    std::cout <<
      "We calculate the shortest path from node s to node t in a graph."
              << std::endl;
    std::cout << std::endl;


    std::cout << "The id of s is " << g.id(s)<< ", the id of t is "
              << g.id(t) << "." << std::endl;

    std::cout << "Dijkstra algorithm demo..." << std::endl;

    Dijkstra<Graph, LengthMap> dijkstra_test(g,len);
    
    dijkstra_test.run(s);
    
    std::cout << "The distance of node t from node s: "
              << dijkstra_test.dist(t) << std::endl;

    std::cout << "The shortest path from s to t goes through the following "
              << "nodes (the first one is t, the last one is s): "
              << std::endl;

    for (Node v=t;v != s; v=dijkstra_test.predNode(v)) {
      std::cout << g.id(v) << "<-";
    }
    
    std::cout << g.id(s) << std::endl;  
    
    return 0;
}