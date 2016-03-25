if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath('__file__'))))

sys.dont_write_bytecode = True


import os
import nltk
import operator
import numpy
from numpy import *
import itertools
import re

from data_utils import utils as du
from msushkov_rnnlm import RNNLM

overnight = True

alltxt = ""
rootdir = "..\\data\\mydata"

a = []
word_vocab = {}

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        with open(filepath, 'r') as myfile:
            data=myfile.read().replace('\n', ' ')
        alltxt = alltxt + " " + data

alltxt = alltxt.replace('"','')
alltxt = alltxt.replace('?','.')
alltxt = alltxt.replace('!','.')
alltxt = alltxt.replace('-',' ')
alltxt = alltxt.replace('. . .','.')
alltxt = alltxt.replace('...','.')

alltxt = alltxt.split('.')

for i in alltxt:
    #Remove non ascii characters
    txt = ''.join(l for l in i if ord(l)<128)
    tokens = nltk.word_tokenize(txt)
    for j in tokens:
        char = j.lower()
        if char in word_vocab:
            word_vocab[char] += 1
        else:
            word_vocab[char] = 1

word_to_num = {}
j = 0
dropped = 0
for i in word_vocab.keys():
    if word_vocab[i] < 5:
        dropped += word_vocab[i]
    else:
        if i not in word_to_num:
            word_to_num[i] = j
            j = j + 1

word_to_num["<s>"] = j
word_to_num["</s>"] = j + 1
mx = j + 1

print "dropped: " +  str(float(dropped)/sum(word_vocab.values()))

num_to_word = du.invert_dict(word_to_num)
vocabsize = len(num_to_word) + 2 #One for line ending and one for unknown


################################
#Prepare data for training.
################################

X_train = []
Y_train = []

for i in alltxt:
    txt = ''.join(l for l in i if ord(l) < 128)
    temparr = [word_to_num["<s>"]] # Start the sentence
    for j in nltk.word_tokenize(txt):
        if j in word_to_num:
            temparr.append(word_to_num[j])
        else:
            temparr.append(mx + 1) #unknown
    if temparr:
        temparr_y = temparr[1:]
        temparr_y.append(mx) #Stop the sentence.
        temparr = numpy.array(temparr)
        temparr_y = numpy.array(temparr_y)
        X_train.append(temparr)
        Y_train.append(temparr_y)

X_train = numpy.array(X_train)
Y_train = numpy.array(Y_train)

################################
#Initialize the model
################################
if overnight:
    hdim = 150
else:
    hdim = 100 # dimension of hidden layer = dimension of word vectors


L0 = zeros((vocabsize, hdim)) # replace with random init, 
                              # or do in RNNLM.__init__()

if overnight:
    model = RNNLM(L0, U0 = L0, alpha=0.1, rseed=10, bptt=15)
else:
    model = RNNLM(L0, U0 = L0, alpha=0.1, rseed=10, bptt=3)


ntrain = len(Y_train)
X = X_train[:ntrain]
Y = Y_train[:ntrain]

k = 5
indices = range(ntrain)

# A random schedule of N/k minibatches of size k, sampled with replacement from the training set.
def idxiter_batches():
    num_batches = ntrain / k
    for i in xrange(num_batches):
        yield random.choice(indices, k)

################################
#Train the model.
################################
print "##########################"
model_output = model.train_sgd(X = X, y = Y, idxiter = idxiter_batches(), printevery = 5000, costevery = 100000)
#Took 156853.67 secs or 43 hours on desktop.
print "##########################"
'''
Begin SGD...
  Seen 0 in 0.01 s
  [0]: mean loss 12.1202
  Seen 5000 in 36342.98 s
  Seen 10000 in 72651.84 s
  Seen 15000 in 81484.19 s
  Seen 20000 in 89962.91 s
  Seen 25000 in 103341.66 s
  Seen 30000 in 112325.85 s
  Seen 35000 in 126391.12 s
  [37385]: mean loss 4.72297
SGD complete: 37385 examples in 156853.67 seconds.
'''

################################
#Generate some sentences.
################################
num_to_word[max(num_to_word.keys())+1] = "UNKKKK"

def seq_to_words(seq):
    return [num_to_word[s] for s in seq]

seq, J = model.generate_sequence(word_to_num["<s>"], word_to_num["</s>"], maxlen=100)

print J
# print seq
print " ".join(seq_to_words(seq))

from nn.math import MultinomialSampler, multinomial_sample

def fill_unknowns(words):
    #### YOUR CODE HERE ####
    word_list = word_vocab.keys()
    word_freqs = word_vocab.values()
    words_and_freqs = zip(word_list, word_freqs)
    new_words = []
    new_freqs = []
    for (w, f) in words_and_freqs:
        if w not in word_to_num:
            new_words.append(w)
            new_freqs.append(f)
    # normalize new_freqs
    s = sum(new_freqs)
    new_freqs = [x / float(s) for x in new_freqs]
    ret = []
    for word in words:
        curr = None
        if word == 'UNKKKK':
            curr = random.choice(new_words, p = new_freqs)
        else:
            curr = word
        ret.append(curr)
    #### END YOUR CODE ####
    return ret

seq, J = model.generate_sequence(word_to_num["<s>"], word_to_num["</s>"], maxlen=100)

print " ".join(fill_unknowns(seq_to_words(seq)))


