'''
Created on Sep 21, 2010

@author: simao
'''
import unittest

import lxbus
import re
from lxbus import LXBUS_REQ_REGEX

class Test(unittest.TestCase):

    def testRequestidRegex(self):
        
        textstr = u"""
                        SMS <span class="il">Carris</span></h1>
                <h3>Pedido realizado em 2010-03-25 09:20  - C 50011</h3>
                
                <table border="0" cellpadding="0" cellspacing="0" width="80%">
                  <tbody><tr>
                    <td colspan="1">
                     <div> 
                        <table border="1" cellpadding="0" cellspacing="0">
                          <tbody><tr style="background-color: rgb(255, 204, 0);"><th colspan="1">Carreira</th>
                
                          <th colspan="1" width="300">Destino</th>
                          <th width="120">Hora Prevista</th>
                          <th width="130">Tempo de Espera</th>
                          </tr>
                        <tr><th>47</th><th>PONTINHA-METRO</th><th>9:22</th><th>01m</th></tr><tr><th>78</th><th>P.LUMIAR</th><th>9:28</th><th>07m</th></tr><tr><th>767</th><th>DAMAIA</th><th>9:30</th><th>09m</th></tr><tr><th>47</th><th>PONTINHA-METRO</th>
                
                
                LXBUS_RQID_PREFIX_MYID_LXBUS_RQID_SUFFIX
                
                <th>9:36</th><th>15m</th></tr><tr><th>47</th><th>PONTINHA-METRO</th><th>9:42</th><th>21m</th></tr><tr><th>78</th><th>P.LUMIAR</th><th>9:46</th><th>25m</th></tr><tr><th>47</th><th>PONTINHA-METRO</th><th>9:52</th><th>31m</th>
                
                
                </tr><tr><th>767</th><th>DAMAIA</th><th>9:53</th><th>32m</th></tr><tr><th>767</th><th>DAMAIA</th><th>9:55</th><th>34m</th></tr>        
                        </tbody></table>    
                      </div>
                
                    </td>
                  </tr>
                  <tr><td> 
                    </td><th colspan="1"></th>
                  
                </tr></tbody></table>
                <p>&nbsp;</p>
        """
        m = LXBUS_REQ_REGEX.search(textstr) 
        
        assert m != None
        
        assert m.group("requestid") == "MYID"

    def testCarrisRegex(self):
        textstr = u"""
                INFO     2010-09-21 22:10:04,501 lxbus.py:31] <h1>SMS Carris</h1>
                <h3>Pedido realizado em 2010-09-21 21:01  - C 10503</h3>
                
                <table border="0" cellpadding="0" cellspacing="0" width="80%">
                  <tbody><tr>
                    <td colspan="1">
                     <div> 
                        <table border="1" cellpadding="0" cellspacing="0">
                          <tbody><tr style="background-color: rgb(255, 204, 0);"><th colspan="1">Carreira</th>
                
                          <th colspan="1" width="300">Destino</th>
                          <th width="120">Hora Prevista</th>
                          <th width="130">Tempo de Espera</th>
                          </tr>
                        <tr><th>790</th><th>PR. REAL</th><th>21:06</th><th>04m</th></tr><tr><th>758</th><th>PORTAS BENFICA</th><th>21:10</th><th>09m</th></tr><tr><th>790</th><th>PR. REAL</th><th>21:14</th><th>13m</th></tr><tr><th>758</th><th>PORTAS BENFICA</th><th>21:21</th><th>19m</th></tr><tr><th>790</th><th>PR. REAL</th><th>21:29</th><th>28m</th></tr><tr><th>758</th><th>PORTAS BENFICA</th><th>21:38</th><th>36m</th></tr><tr><th>758</th><th>SETE RIOS</th><th>21:49</th><th>47m</th></tr><tr><th>758</th><th>SETE RIOS</th><th>22:09</th><th>68m</th></tr>        
                        </tbody></table>    
                      </div>
                
                    </td>
                  </tr>
                  <tr><td> 
                    </td><th colspan="1"></th>
                  
                </tr></tbody></table>
                
                <p>&nbsp;</p>
        """
        pattern = re.compile(lxbus.CARRIS_REGEX)
        matches = pattern.finditer(textstr)
        
        for bnr in matches:
            assert(int(bnr.group(1)) > 0)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCarrisRegex']
    unittest.main()