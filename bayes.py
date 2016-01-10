'''
Created on May 18, 2015

@author: pmj812

'''
import BN
import numpy as np

net = BN.network()
net.addNode('A',['a1','a2']          ,[],np.array([ 0.9,  0.1]))
net.addNode('C',['c1','c2','c3','c4'],[],np.array([ 0.1,  0.2,  0.3,  0.4]))

bCPT = np.array(
      [[[0.2, 0.1, 0.01, 0.2], [0.33, 0.3, 0.2, 0.9 ]],
       [[0.4, 0.5, 0.01, 0.1], [0.33, 0.1, 0.7, 0.05]],
       [[0.4, 0.4, 0.98, 0.7], [0.34, 0.6, 0.1, 0.05]]])    
                
net.addNode('B',['b1','b2','b3'],['A','C'],bCPT)

def marginal(node):
    print('{} marginal distribution is {}'.format(node, net.getMarginal(node)))
def allMarginals():
    for node in net.vertexes():
        marginal(node)
        
print ("Marginal distributions without evidence")
allMarginals()

print ("\n\nMarginal distributions given B=b3")
net.setEvidence('B','b3')
allMarginals()

print ("\n\nMarginal distributions given B=b3 and C=c4")
net.setEvidence('C','c4')
allMarginals()

print ("\n\nMarginal distributions given C=c4")
net.clearEvidence('B')
allMarginals()
