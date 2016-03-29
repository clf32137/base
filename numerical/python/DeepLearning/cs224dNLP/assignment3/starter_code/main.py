from __future__ import print_function

import sys, os
from numpy import *
from matplotlib.pyplot import *
from rnn import RNN
import collections
import pprint
from nltk.tree import Tree


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath('__file__'))))

sys.dont_write_bytecode = True


###############################
# Take a peek at how the tree works.
###############################
import tree as treeM
train = treeM.loadTrees()

word_to_id = treeM.loadWordMap()
id_to_word = {}
for i in word_to_id:
	id_to_word[word_to_id[i]] = i

treeTxt = ""
def prnt(node):
	global treeTxt
	if node.isLeaf:
		#print(id_to_word[node.word], end = " ")
		treeTxt = treeTxt + id_to_word[node.word] + " "
		return 0
	else:
		treeTxt = treeTxt + "("
		prnt(node.left)
		prnt(node.right)
		treeTxt = treeTxt + ")"

#Print a sentence.
prnt(train[0].root)
nltktree = Tree.fromstring(treeTxt)
nltktree.pretty_print()

###############################
# Create a toy model for testing.
###############################
numW = len(treeM.loadWordMap())

wvecDim = 10
outputDim = 5

rnn = RNN(wvecDim, outputDim, numW, mbSize = 4)
rnn.initParams()

rnn.L, rnn.W, rnn.b, rnn.Ws, rnn.bs = rnn.stack

# Zero gradients
rnn.dW[:] = 0
rnn.db[:] = 0
rnn.dWs[:] = 0
rnn.dbs[:] = 0
rnn.dL = collections.defaultdict(rnn.defaultVec)

ost = 0.0
correct = []
guess = []
total = 0.0

train[0].root.hActs1
print("#############\nrunning forward prop\n##############", end = "\n")
c, tot = rnn.forwardProp(train[0].root, correct, guess)

print("#############\nrunning backward prop\n##############", end = "\n")
rnn.backProp(train[0].root)


