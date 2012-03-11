#!/usr/bin/python
#
# Project : PylearnDico
# Author  : Mickael "Mogmi" Bidon
# Version : 1.1

## TODO
# - Create sentence using the weight of each word
# - Fix errors while parsing some ponctuation
# - Create a more accurate parsing
# - Create a more accurate sentence generation
##

# Module for serialization
import pickle
# Module for Random
import random

class PylearnDico():

    ########
    # Data #
    ########

    ## words
    # List of known words : Map<String, Map<String, Integer>>
    # Special keywords :
    #       - "|BEGIN|" : list of words which begins a sentence
    #       - "|END|" : list of words which ends a sentence
    ##
    words = {}
    beginWord = "|BEGIN|"
    endWord = "|END|"

    ## cutChars
    # List of characters that define a pause in a sentence
    ##
    cutChars = [',', ';', ':']

    ## endChars
    # List of characters that define the end of a sentence
    ##
    cutChars = ['.', '!', '?']

    ## blacklist
    # Words that must not be added into the dictionary
    ##
    blacklist = []

    #############
    # Interface #
    #############

    ## newDico()
    # Create a new PylearnDico, erase the current one
    ##
    def newDico(self):
        self.words = {}

    ## loadDico(string filename)
    # Load PylearnDico from the file filename
    ##
    def loadDico(self, filename):
        loadFile = open(filename, "rb")
        self.words = pickle.load(loadFile)
        loadFile.close()

    ## saveDico(string filename)
    # Save the current dico to the file filename
    ##
    def saveDico(self, filename):
        saveFile = open(filename, "wb")
        pickle.dump(self.words, saveFile)
        saveFile.close()

    ## parse(string sentence)
    # Read a string and learn new word and constructions from it
    ##
    def parse(self, sentence):
        currentWord = 0
        words = sentence.split()
        lastWord = len(words) - 1
        for word in sentence.split():
            # print(word)
            # If first word, we append to BEGIN
            if (currentWord == 0):
                self.addSuccessorToWord(self.beginWord, word)
            # Else we append to the previous word
            else:
                self.addSuccessorToWord(words[currentWord - 1], word)
            # If last word, we append to END
            if (currentWord == lastWord):
                self.addSuccessorToWord(word, self.endWord)
            currentWord += 1
        #print("DONE")
        #print(self.words)

    ## getSentence()
    # Return a string created from words already learned
    ##
    def getSentence(self):
        currentWord = self.getRandomNextWord(self.beginWord)
        sentence = currentWord
        currentWord = self.getRandomNextWord(currentWord)
        while (currentWord != self.endWord):
            sentence += " " + currentWord
            currentWord = self.getRandomNextWord(currentWord)
        return sentence

    ## getSentenceWithName(string login)
    # Return a string which begin with "login"
    ##
    def getSentenceWithName(self, login):
        if not(login in self.words):
            return "Sorry, " + login + " is not present in the database."
        currentWord = login
        sentence = currentWord
        currentWord = self.getRandomNextWord(currentWord)
        while (currentWord != self.endWord):
            sentence += " " + currentWord
            currentWord = self.getRandomNextWord(currentWord)
        return sentence


    ## getStats()
    # Return a string which gives information about the current database,
    # such as number of words
    ##
    def getStats(self):
        return len(self.words)

    ## removeWord(string word)
    # Delete a word from the dico
    ##
    def removeWord(self, word):
        if (word in self.words):
            self.words.remove(word)

    ## blacklistWord(string word)
    # Add a word to the blacklist. Those words won't be stored
    ##
    def blacklistWord(self, word):
        if not(word in self.blacklist):
            self.blacklist.append(word)

    ## unBlacklistWord(string word)
    # Remove a word from the blacklist.
    ##
    def unBlacklistWord(self, word):
        if not(word in self.blacklist):
            self.blacklist.remove(word)

    ## getBlackList()
    # Return list of blacklisted words
    ##
    def getBlacklist(self):
        return self.blacklist

    #############
    # Functions #
    #############

    ## addSuccessorToWord(string word, string successor)
    # Add the string successor as a potential next to word
    ##
    def addSuccessorToWord(self, word, successor):
        if not(word in self.words):
            self.words[word] = {}
        if (successor in self.words[word]):
            self.words[word][successor] += 1
        else:
            self.words[word][successor] = 1

    ## getRandomNextWord(string word)
    # Return a word who can follow 'word'
    ##
    def getRandomNextWord(self, word):
        ## A working but too simple algorithm
        #result = random.choice(list(self.words[word].keys()))
        ##

        ## This one is better, but awful
        wordList = []
        for key, weight in self.words[word].items():
            for i in range(0, weight):
                wordList.append(key)
        result = random.choice(wordList)
        return result
