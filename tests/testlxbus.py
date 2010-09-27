'''
Created on Sep 21, 2010

@author: simao

-*- coding: utf-8 -*-
'''
import unittest

import lxbus

class Test(unittest.TestCase):
    
    
    def testCarrisSubjectRegex(self):
        textstr = u" 2010-09-25 18:10 >C 10503<"
        
        stopcode = lxbus.CARRIS_SUBJECT_REGEX.search(textstr).group("stopcode")

        assert stopcode == "10503"
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCarrisRegex']
    unittest.main()