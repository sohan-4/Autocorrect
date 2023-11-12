# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 21:13:13 2022

@author: Sohan Biswal
"""

'''

This is an autocorrect, it checks for possible spelling mistakes, if it cannot find a word in its dictionary
then it delete's a letter, inserts a letter, swaps letters, and replaces letters with keys next to a key
on the keyboard to look for possible replacements, it outputs the amount of possible replacements and at most
the three most common replacements. The file words.txt from where it gets its words is not expansive and does not
include all the words in the English language so this autocorrect is not expansive. words.txt and keyboard.txt
need to be in the same folder as this program for it to work.

'''

import string
import sys

def file_to_dict(fname, splitC):
    
    my_file=open(fname, 'r')
    my_dict=dict()
    
    #go through file and assign the line elements to a list
    for line in my_file:
        
        line=line.strip()
        
        if line=="":
            return my_dict
        
        line_elements=line.split(splitC)
        
        for i in range(len(line_elements)):
            line_elements[i].strip()
        
        my_dict[line_elements[0]]=line_elements[1]
    
    my_file.close()
    return my_dict

def check_word(iword, iwd, ikb):
    
    cwords=set()
    found=True
    
    if iword in iwd:#found
        return cwords, found
    else:
        
        found=False
        
        #drop
        for i in range(len(iword)):
            new_word=list(iword)#i assign new_word to iword in the data form i need because in change i want to modify them i dont want it to mexx up my indices
            new_word.pop(i)
            if ''.join(new_word) in iwd:
                cwords.add(''.join(new_word))
        
        #insert
        alphabet = list(string.ascii_lowercase)
        for i in range(len(alphabet)):
            new_word=list(iword)
            for j in range(len(new_word)):
                new_word=list(iword)
                new_word.insert(j, alphabet[i])
                if ''.join(new_word) in iwd:
                    cwords.add(''.join(new_word))
            new_word=list(iword)
            new_word.append(alphabet[i])
            if ''.join(new_word) in iwd:
                cwords.add(''.join(new_word))
        
        #swap
        for i in range(len(iword)):
            new_word=list(iword)
            if i+1<len(new_word):
                new_word[i], new_word[i+1]=new_word[i+1], new_word[i]
                if ''.join(new_word) in iwd:
                    cwords.add(''.join(new_word))
        
        #replace
        for i in range(len(iword)):
            new_word=iword
            letter=new_word[i]
            letters=ikb[letter]
            for j in range(len(letters)):
                new_word=list(iword)
                new_word[i]=letters[j]
                if ''.join(new_word) in iwd:
                    cwords.add(''.join(new_word))
        
        return cwords, found

if __name__ == "__main__":
    
    ifile_name = sys.argv[1]
    
    #get dict files
    word_dict=file_to_dict("words.txt", ',')
    
    #get input file
    ifile=open(ifile_name, 'r')
    words=[]
    for i in ifile:
        
        i=i.strip()
        
        if i == "":
            break
        
        words.append(i)
    
    ifile.close()
    
    kb=dict()
    #get keyboard file
    kbfile=open("keyboard.txt", 'r')
    for i in kbfile:
        i=i.strip()
        
        if i == "":
            break
        
        line_list=i.split()
        letter=line_list[0]
        line_list.pop(0)
        kb[letter]=line_list
        
    kbfile.close()
    
    #start printing the output
    corrections=[]
    word_cw=dict()
    for i in range(len(words)):
        word=words[i]
        word_cw[word], found = check_word(word, word_dict, kb)
        
        if len(word_cw[word])==0:
            #if the word was correct
            if found:
                corrections.append("valid")
            #if the word was incorrect and no correct candidates were found
            else:
                corrections.append("invalid")
        
        #if the word was incorrect and correct candidates were found
        else:
            #getting the correct candidates
            this_word_list=word_cw[word]
            #sorting them
            word_pop = dict()
            for j in this_word_list:
                word_pop[j] = word_dict[j]
                
            word_pop = dict(sorted(word_pop.items(), key=lambda item: float(item[1])))
                
            sorted_words = []
            
            for j in word_pop:
                sorted_words.append(j)
                
            corrections.append(sorted_words)
            
    #open output file
    output_file_name = sys.argv[2]
    ofile = open(output_file_name, 'w')
    
    for i in range(len(corrections)):
        if type(corrections[i]) is str:
            print(corrections[i], file = ofile)
        else:
            print("invalid", end='', file = ofile)
            for j in range(len(corrections[i])):
                print(','+corrections[i][j], file = ofile, end='')
                
            print(file = ofile)