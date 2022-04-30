# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:21:04 2022

@author: determinant
"""

"""
This script corrects a 10-digit ISBN code in the following way:
    - it detects whether the code seems to be correct
    - if potentially correct, find the book and print the title (THIS MIGHT FAIL)
    - if detected as incorrect, try correcting it 
In our book it is assumed errors only happen as a switch of consecutive values, 
i.e. 3540(4)(6)1335 could be 3540(6)(4)1335, and the only check it was explained 
in the book is the verification of the code equation.

This script ignores 13-digit ISBNs.

The reason of these assumptions is that I just wrote it to solve an exercise 
in the book itself (Codes, Cryptology and Curves with Computer Algebra), hence I shall follow its assumptions.

"""

import re


def cleanIsbnCode(isbncode):
    # isbncode is a string
    # returns a list consisting of integers (i.e. edits X occurrences)
    isbnlist = [i for i in isbncode]
    if "X" in isbnlist:
        isbnlist[isbnlist.index("X")] = 10
    return isbnlist

def codeEquation(isbnlist):
    # returns the output of the code equation for 10-digit ISBNs
    n = len(isbnlist)
    return sum([(i+1)*int(isbnlist[i]) for i in range(n)]) % 11

def isCorrect(isbn):
    # verifies if a string isbn is a (potentially) valid 10-digit ISBN code
    isbncode = cleanIsbnCode(isbn)
    n = len(isbncode)
    # print(f"     > code {isbncode}")
    assert n == 10,f"invalid ISBN code {isbn}, length {len(isbn)} should be 10"
    return codeEquation(isbncode) == 0

def check(code):
    print("------------------------------")
    # cleaning input:
    isbn = re.sub("[^ 0,1,2,3,4,5,6,7,8,9,X]", "", code)
    print(f"     > code {isbn} detected")
        
    # validity verification:    
    if not isCorrect(isbn) :
        print("     > invalid code")
        # we suppose two consecutive characters have been swapped...
        candidates = [] # < candidate valid ISBNs
        code = cleanIsbnCode(isbn)
        print("     > searching for candidate codes")
        for i in range(9):
            j = i+1
            candidate = code.copy()
            candidate[i],candidate[j] = candidate[j],candidate[i]
            if isCorrect(candidate) :
                candidates.append("".join(candidate))
        for can in candidates :
            print(f"     > {can} ")
            print(f"         > {isbnFinder(can)} ")
    else :
        print("     > valid code")
        print(f"        > {isbnFinder(isbn)} ")
        
        
import urllib.request
import json
import textwrap

    
def isbnFinder(isbn):
    """
    algorithm adapted from 
    https://gist.github.com/AO8/faa3f52d3d5eac63820cfa7ec2b24aa7
    """
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    while True:

        with urllib.request.urlopen(base_api_link + isbn) as f:
            text = f.read()

        decoded_text = text.decode("utf-8")
        obj = json.loads(decoded_text) # deserializes decoded_text to a Python object
        
        """ 
        my ISBN codes could be invalid, I need to code the following:
        """
        isvalid_dict =  "items" in obj
        
        if isvalid_dict:
            volume_info = obj["items"][0] 
            return volume_info["volumeInfo"]["title"]
        else :
            return "invalid volume"
        
        
        
        

        
if __name__ == "__main__":
    validisbn = "192660668X" # < A Study in Scarlet, Conan Doyle
    validisbn2 = "192660668X" # < A Study in Scarlet, Conan Doyle
    invalidisbn = "3540461335" # < given by our textbook
    invalidisbn2 = "3-540-4613-35"
    invalidisbn3 = "1318197017" # < modified ISBN code for the book Stinson-Paterson
    
    check(validisbn)
    check(invalidisbn)
    check(invalidisbn2)
    check(invalidisbn3)