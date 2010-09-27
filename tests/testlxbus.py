'''
Created on Sep 21, 2010

@author: simao

-*- coding: utf-8 -*-
'''
import unittest

from BeautifulSoup import BeautifulSoup

import lxbus
import re
import codecs

class Test(unittest.TestCase):
    
    
    def testParsingWithBS(self):
        
        f = codecs.open("test.html", "r", "utf-8")
        
        textstr = f.read()
        
        soup = BeautifulSoup(textstr)
        
        print soup.prettify()
                     
    
    def testCarrisSubjectRegex(self):
        textstr = u" 2010-09-25 18:10 >C 10503<"
        
        stopcode = lxbus.CARRIS_SUBJECT_REGEX.search(textstr).group("stopcode")

        assert stopcode == "10503"
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCarrisRegex']
    unittest.main()