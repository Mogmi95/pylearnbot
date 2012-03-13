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
    begin_word = "|BEGIN|"
    end_word = "|END|"

    ## cut_chars
    # List of characters that define a pause in a sentence
    ##
    cut_chars = [',;:']

    ## end_chars
    # List of characters that define the end of a sentence
    ##
    end_chars = ['.!?']

    ## blacklist
    # Words that must not be added into the dictionary
    ##
    blacklist = []

    #############
    # Interface #
    #############

    ## new_dico()
    # Create a new PylearnDico, erase the current one
    ##
    def new_dico(self):
        self.words = {}

    ## load_dico(string filename)
    # Load PylearnDico from the file filename
    ##
    def load_dico(self, filename):
        load_file = open(filename, "rb")
        self.words = pickle.load(load_file)
        load_file.close()

    ## save_dico(string filename)
    # Save the current dico to the file filename
    ##
    def save_dico(self, filename):
        save_file = open(filename, "wb")
        pickle.dump(self.words, save_file)
        save_file.close()

    ## parse(string sentence)
    # Read a string and learn new word and constructions from it
    ##
    def parse(self, sentence):
        sentences = sentence.split(self.end_chars)
        for sentence in sentences:
            current_word = 0
            words = sentence.split(self.end_chars)
            last_word = len(words) - 1
            for word in sentence.split():
                # print(word)
                # If first word, we append to BEGIN
                if (current_word == 0):
                    self.add_successor_to_word(self.begin_word, word)
                # Else we append to the previous word
                else:
                    self.add_successor_to_word(words[current_word - 1], word)
                # If last word, we append to END
                if (current_word == last_word):
                    self.add_successor_to_word(word, self.end_word)
                current_word += 1
            #print("DONE")
            #print(self.words)

    ## get_sentence()
    # Return a string created from words already learned
    ##
    def get_sentence(self):
        current_word = self.get_random_next_word(self.begin_word)
        sentence = current_word
        current_word = self.get_random_next_word(current_word)
        while (current_word != self.end_word):
            sentence += " " + current_word
            current_word = self.get_random_next_word(current_word)
        return sentence

    ## get_sentence_with_name(string login)
    # Return a string which begin with "login"
    ##
    def get_sentence_with_name(self, login):
        if not(login in self.words):
            return "Sorry, " + login + " is not present in the database."
        current_word = login
        sentence = current_word
        current_word = self.get_random_next_word(current_word)
        while (current_word != self.end_word):
            sentence += " " + current_word
            current_word = self.get_random_next_word(current_word)
        return sentence


    ## get_stats()
    # Return a string which gives information about the current database,
    # such as number of words
    ##
    def get_stats(self):
        return len(self.words)

    ## remove_word(string word)
    # Delete a word from the dico
    ##
    def remove_word(self, word):
        if (word in self.words):
            self.words.remove(word)

    ## blacklist_word(string word)
    # Add a word to the blacklist. Those words won't be stored
    ##
    def blacklist_word(self, word):
        if not(word in self.blacklist):
            self.blacklist.append(word)

    ## un_blacklist_word(string word)
    # Remove a word from the blacklist.
    ##
    def un_blacklist_bord(self, word):
        self.blacklist.remove(word)

    ## get_blackList()
    # Return list of blacklisted words
    ##
    def get_blacklist(self):
        return self.blacklist

    #############
    # Functions #
    #############

    ## add_successor_to_word(string word, string successor)
    # Add the string successor as a potential next to word
    ##
    def add_successor_to_word(self, word, successor):
        if not(word in self.words):
            self.words[word] = {}
        if (successor in self.words[word]):
            self.words[word][successor] += 1
        else:
            self.words[word][successor] = 1

    ## get_random_next_word(string word)
    # Return a word who can follow 'word'
    ##
    def get_random_next_word(self, word):
        ## A working but too simple algorithm
        #result = random.choice(list(self.words[word].keys()))
        ##

        ## This one is better, but awful
        word_list = []
        for key, weight in self.words[word].items():
            for i in range(0, weight):
                word_list.append(key)
        result = random.choice(word_list)
        return result
