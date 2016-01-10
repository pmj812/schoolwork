'''
Created on May 18, 2015

@author: pmj812
'''

import graph
import numpy as np

class network(graph.DirectedGraph):


    def addNode(self, name, values, parents, cpt):
  
        if name in self.vertexes():
            raise ValueError("Node {} already in network".format(name))
        if len(parents) != cpt.ndim-1:
            raise ValueError("{} parents specified but CPT has {} dimensions".format(len(parents),cpt.ndim))
        v = self.addVertex(name)
        v.values = values
        v.cpt = cpt
        for parent in parents:
            if parent not in self.vertexes():
                raise ValueError("Please add parent node {} before adding child node {}".format(parent,v))
            self.addEdge(parent, name)
        # assign a character for einsum operations with this node
        v.einsumChar = chr(64+len(self.vertexes())) # ascii 65 is 'A'
        v.eisumCPTChars = v.einsumChar + ''.join([parent.einsumChar for parent in v.neighbors])
        v.evidence = None
            
        # validate sizes of the CPT's    
        if len(values) != cpt.shape[0]:
            raise ValueError("{} values specified but CPT[0] has length {}".format(len(values),cpt.shape[0]))      
        for parent, cptDimLen in zip(v.neighbors,v.cpt.shape[1:]):
            if len(parent.values) != cptDimLen:
                raise ValueError("Node {} has {} values specified but corresponding CPT dimension in child {} has length {}".
                                 format(parent, len(parent.values), v,cptDimLen))
        
        
    def setEvidence(self,name,value):
        try:
            v = self.getVertex(name)
        except:
            raise ValueError("Unknown node {}".format(name))     
        try:
            v.evidence = np.zeros(len(v.values))
            v.evidence[v.values.index(value)] = 1 # Put a one (certainty) where we know the value is
        except:
            raise ValueError("{} is not a valid value for node {}".format(value))
        
    def clearEvidence(self,name):

        try:
            v = self.getVertex(name)
            v.evidence = None
        except:
            raise ValueError("Unknown node {}".format(name))
        
    def getMarginal(self,name):

        try:
            v = self.getVertex(name)
        except:
            raise ValueError("Unknown node {}".format(name))
        
        einSumStrings = [v.eisumCPTChars for v in self.vertexes()]
        einSumPotentials = [v.cpt for v in self.vertexes()]
        
        # Add evidence potentials for variables where evidence is not None
        einSumEvidenceStrings = [v.einsumChar for v in self.vertexes() if v.evidence!=None]
        einSumEvidencePotentials = [v.evidence for v in self.vertexes() if v.evidence!=None ]
        vMarginal = np.einsum(','.join(einSumStrings+einSumEvidenceStrings)+'->'+v.einsumChar,*(einSumPotentials+einSumEvidencePotentials))
        
        # normalize the distribution obtained
        return vMarginal/np.sum(vMarginal)
        
            
        
