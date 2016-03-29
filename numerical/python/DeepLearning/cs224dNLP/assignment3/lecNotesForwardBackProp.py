import numpy as np
import collections
import pdb



class RNNClassNotes:
	def forwardProp(self,node):
		#Recursion
		#...

		#This nodes hidden activation
		node.h = np.dot(self.W, np.hstack([node.left.h, node.right.h])) + self.b

		#Relu
		node.h[node.h<0] = 0

		#Softmax
		node.probs = np.dot(self.Ws,node.h) + self.bs
		node.probs -= np.max(node.probs)
		node.probs = np.exp(node.probs)
		node.probs = node.probs/np.sum(node.probs)

	def backwardProp(self,node):
		#Softmax grad
		deltas = node.probs
		deltas[node.label] -= 1.0;
		

