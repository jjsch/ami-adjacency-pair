from collections import defaultdict
import nltk
import csv
import os
import re

def digram(dig,words):
    '''checks whether the digram dig is in the list words'''
    if len(words) < 2:
        return False
    tup = dig.lower().split(" ")
    for i in range(len(words)-1):
        if words[i] == tup[0] and words[i+1] == tup[1]:
            return True
    return False

def trigram(trig,words):
    '''checks whether the trigram trig is in the list words'''
    if len(words) < 3:
        return False
    trip = trig.lower().split(" ")
    for i in range(len(words)-2):
        if words[i] == trip[0] and words[i+1] == trip[1] and words[i+2] == trip[2]:
            return True
    return False

def containsNegation(corpus,i):
    '''checks whether the utterance at index i contains a negation'''
    words = corpus[i][6].split(" ")
    words = [word.lower() for word in words]
    for j in range(len(words)):
        if words[j].endswith("n't") or words[j] in ["not"]:
            return True
    return False

def normalize(word,stemmer):
    if word == "n't":
        return "not"
    if word == "'s":
        return "is"
    return stemmer.stem(word.lower())

def removeStopwords(words):
    stopwords = list(nltk.corpus.stopwords.words('english'))
    newwords = []
    for word in words:
        if not word in stopwords:
            newwords.append(word)
    return newwords

def findTurn(corpus,i):
    '''computes the dialogue turn that the utterance at index i is in.'''
    speaker = corpus[i][5]
    start = i
    end = i+1
    length = 1
    while True:
        try:
            if corpus[end][5] == speaker:
                end += 1
                length += 1
            elif corpus[end][2] in ['bck','fra']:
                end += 1
            else:
                break
        except IndexError:
            break

    while True:
        try:
            if corpus[start-1][5] == speaker:
                start -= 1
                length += 1
            elif corpus[start-1][2] in ['bck','fra']:
                start -= 1
            else:
                break
        except IndexError:
            break

    while True:
        try:
            if not corpus[start][5] == speaker:
                start += 1
            else:
                break
        except IndexError:
            break

    while True:
        try:
            if not corpus[end-1][5] == speaker:
                end -= 1
            else:
                break
        except IndexError:
            break

    return (start,end,length)

def findTarget(corpus,i):
    '''if the utterance at index i is a second-part of an adjacency pair, returns the index of the first part. Otherwise returns i.'''
    if not corpus[i][3] in ['POS','NEG']:
        return i
    if corpus[i][4] == '-':
        return i
    timestamp = corpus[i][4]
    index = corpus[i][0]
    for k in range(i):
        if corpus[k][1] == timestamp and corpus[k][0] == index:
            return k
    return i

def findNext(corpus,i,speaker):
    '''finds first utterance of next turn'''
    for k in range(i+1,len(corpus)):
        if corpus[k][5] == speaker and (not corpus[k][2] in ['bck','fra']):
            return k
    return i

def isWord(word):
    return (re.match("^['\w-]+$",word) is not None)

def findWords(corpus,i,lower=True):
    '''computes the list of words corresponding to the surface form of an utterance'''
    candidates = corpus[i][6].split(" ")
    retVal = []
    for s in candidates:
        if isWord(s):
            if lower:
                retVal.append(s.strip().lower())
            else:
                retVal.append(s.strip())
    return retVal

def prettyPrint(corpus,start,end,mark):
    '''pretty print for debugging'''
    for i in range(start,end):
        utt = corpus[i]
        if not i == mark:
            print utt[2]+" "+utt[5]+": "+utt[6]
        else:
            print utt[3]+" "+utt[2]+" "+utt[5]+": "+utt[6]


def getCorpus:
    obsv = os.listdir('csv')
    mistags = [] # to exclude mis-annotated observations
    corpus = {}
    index = 0
    for obs in obsv:
        obsname = obs.split("-")[0]
        if obsname in mistags:
            continue
        corpus[obs] = []
        with open('csv/'+obs) as csvfile:
            reader = csv.reader(csvfile,delimiter="\t",quotechar='"')
            i = 0
            for row in reader:
                i += 1
                if i < 4:
                    continue
                row2 = [index]
                for element in row:
                    row2.append(element.strip())
                corpus[obs].append(row2)
        index += 1
    return corpus
