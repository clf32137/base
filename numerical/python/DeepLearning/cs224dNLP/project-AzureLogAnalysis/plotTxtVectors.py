import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.spatial import distance
from random import sample
from kmeans import *
from opticsv0 import *
import sys
####################
#Arg1 - How many dimensional vectors should I train?
#Arg2 - Path of file where the text vectors are stored.
####################

class plotVecs:
	#regexs - a string array of regexs we want to explore.
	def __init__(self, vectorDimLen = 200, pathOfVectors="data\\agentlogsVecsAscii.txt", regexs=["container", "__HEX__"]):
		self.pathOfVectors = pathOfVectors
		self.vectorDimLen = vectorDimLen
		self.regexs = regexs
		self.regexNumElements = [0 for k in xrange(len(regexs) + 1)]
		self.regexMap = [{} for k in xrange(len(regexs) + 1)]
		self.vectorDict = {}
		self.X = []
		self.rawLogs = []
		self.createDictionary()
		self.createPlot()
		

	def createDictionary(self):
		f = open(self.pathOfVectors)
		for i in f:
		    strarr = i.split(' ')
		    if len(strarr) == self.vectorDimLen + 2:
		        data = []
		        for j in xrange(1, (self.vectorDimLen + 1)):
		            data.append(float(strarr[j]))
		        data = np.array(data)
		        hashedLog = self.hashregexNumElements(strarr[0])
		        self.vectorDict[hashedLog] = data
		        self.X.append(data)
		        self.rawLogs.append(strarr[0])

	def hashregexNumElements(self, logToHash):
		hashedStr = ""
		for i in xrange(len(self.regexs)):
		#This will check each key before going to the catch all but thats ok since we should be testing a small number of them for plotting
			if self.regexs[i] in logToHash:
				hashedStr = self.regexs[i] + str(self.regexNumElements[i])
				self.regexMap[i][self.regexNumElements[i]] = logToHash
				self.regexNumElements[i] = self.regexNumElements[i] + 1
				break
		#If we still didn't assign a hash, call it 'other'
		if len(hashedStr) == 0:
			hashedStr = "other" + str(self.regexNumElements[i+1])
			self.regexMap[i+1][self.regexNumElements[i+1]] = logToHash
			self.regexNumElements[i+1] = self.regexNumElements[i+1] + 1
		return hashedStr

	def createPlot(self):
		print "Elelemnts in each group:" + str(self.regexNumElements) + "\n##############\n"
		visualizeWords = self.generateWordsToPlot()
		visualizeVecs = []
		for i in visualizeWords:
		    visualizeVecs.append(self.vectorDict[i])

		visualizeVecs = np.array(visualizeVecs)

		temp = (visualizeVecs - np.mean(visualizeVecs, axis=0))
		covariance = 1.0 / len(visualizeWords) * temp.T.dot(temp)
		U,S,V = np.linalg.svd(covariance)
		coord = temp.dot(U[:,0:2])

		for i in xrange(len(visualizeWords)):
		    plt.text(coord[i,0], coord[i,1], visualizeWords[i], bbox=dict(facecolor='green', alpha=0.1))

		plt.xlim((np.min(coord[:,0]), np.max(coord[:,0])))
		plt.ylim((np.min(coord[:,1]), np.max(coord[:,1])))
		plt.show()

	#Generates some random candidates to plot.
	def generateWordsToPlot(self, samplesOfEach = 3, samplesOfOther = 1):
		visualizeWords = []
		for i in xrange(len(self.regexs)):
			for j in sample(xrange(int(self.regexNumElements[i])), samplesOfEach):
				visualizeWords.append( self.regexs[i] + str(j))
				print self.regexs[i] + str(j) + ":" + self.regexMap[i][j] + "\n\n"
		for j in sample(xrange(int(self.regexNumElements[i+1])), samplesOfOther):
			visualizeWords.append( "other" + str(j))

		return visualizeWords


def splitClusterWords(logList):
	words = {}
	for i in logList:
		for j in i.split("--"):
			if j in words:
				words[j] = words[j] + 1
			else:
				words[j] = 1
	printDictReverse(words)
	
def printDictReverse(words, printEntries = 25):
	j = 0
	for k in sorted(words, key = words.get, reverse=True):
		print (k, words[k])
		j = j + 1
		if j>printEntries:
			print("\nVocab size = " + str(len(words)) + "\n")
			break


if __name__ == "__main__":
	#Assign values to all arguments.
	pathOfVectors = "data\\agentlogsVecsAscii.txt" #By default
	vectorDimLen = 200 #By default
	regexs = ["diskhealthmonitor", "createcontainer"] #By default
	if len(sys.argv) > 1:
		vectorDimLen = int(sys.argv[1])

	if len(sys.argv) > 2:
		pathOfVectors = sys.argv[2]

	if len(sys.argv) > 3:
		regexs = sys.argv[3:]

	print "vector dimension should be: " + str(vectorDimLen)
	pv = plotVecs(vectorDimLen, pathOfVectors, regexs)
	#Try k-means clustering
	k = 3
	res = kmeans(pv.X,np.array(sample(pv.X, k)))
	for i in xrange(k):
		splitClusterWords(np.array(pv.rawLogs)[res[1] == i])
	#Give optics a shot
	pv.X = np.array(pv.X)
	optics(pv.X)

