'''
Created on Apr 19, 2015

@author: pmj812

'''

import collections
import functools

@functools.total_ordering
class _Vertex(object):
   
    def __init__(self, name):
        
        
        self.name = name
        self.neighbors = collections.OrderedDict() 
        # the Vertexes that this Vertex is connected to via Edges. (The parents of this node in a directed graph)
        # note that python does not have an OrderedSet natively, but an OrderedDict will work for our purposes

  
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self,other):
        try:
            return self.name == other.name        
        except:
            return self.name == other # in case other is a string
    def __lt__(self,other):
        return self.name < other.name
    
    def __repr__(self):
        return str(self.name)
    
@functools.total_ordering
class _Edge(object):

    def __init__(self, p, c, weight=1):

        self.p = p           
        self.c = c          
        self.weight = weight
        
  
    def __hash__(self):
        return hash((self.p,self.c)) 
        
    def __eq__(self,other):
        return (self.p,self.c) == (other.p,other.c) 
                  
    def __lt__(self,other):
        return (self.p,self.c) < (other.p,other.c) 
        
    def __repr__(self):
        return str((self.p,self.c))
    
class DirectedGraph(object):

    
    def addVertex(self,name):

        if name not in self._vertexes:
            self._vertexes[name] = _Vertex(name)
        return self._vertexes[name]
            
    def addEdge(self,pName,cName,weight=1):
      
        if (pName,cName) not in self._edges:
            p = self.addVertex(pName) # addVertex is idempotent!
            c = self.addVertex(cName)
            c.neighbors[p] = None
            self._edges[(pName,cName)] = _Edge(p,c, weight)
        return self._edges[(pName,cName)]
    
    def vertexes(self):

        return self._vertexes.values() 
    
    def getVertex(self,name):

        return self._vertexes[name] 

    def edges(self):

        return self._edges.values() 

    def __init__(self, vertexes = [], edges = []):
        self._vertexes = {}
        for v in vertexes:
            self.addVertex(v)
             
        self._edges = {}
        for e in edges:
            self.addEdge(*e)
            
    def __repr__(self):
        return 'DirectedGraph: [{}]'.format(', '.join([str(k) for k in sorted(self._edges.items())]))
    
class UndirectedGraph(DirectedGraph):

            
    def addEdge(self,uName,vName,weight=1):

        uName,vName = (uName,vName) if uName<vName else (vName,uName) # canonical orientation for the edge
        edge = super().addEdge(uName,vName,weight) 
        self._vertexes[uName].neighbors[self._vertexes[vName]] = None
        return edge
    
    def __repr__(self):
        return 'UndirectedGraph: [{}]'.format(', '.join([str(k) for k in sorted(self._edges.values())]))


