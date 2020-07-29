#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:07:56 2020

@author: zoakes
"""

#Testing ...
import pytest
from OptimizeInitialMargin import InitialMarginOptimizer





def test_dict_replace_and_add(new_dict, new_pair):
    #Initialize...
    imo = InitialMarginOptimizer(40)
    imo.futures_dict = {'NQ':20}
    
    #Test replace...
    imo.futures_dict = new_dict
    assert imo.futures_dict == pytest.approx(new_dict) , 'Replace -- Tuple Arg -- not working.'
    print(imo.futures_dict,'==',new_dict)

    #Test 'Append'
    imo.futures_dict = new_pair

    assert list(imo.futures_dict.keys())[1] == new_pair[0]
    assert len(imo.futures_dict) == 2
    
    #Test sort...
    a = sorted(imo.futures_dict.items(),key=lambda x: x[1], reverse=True)
    b = list(imo.futures_dict.items())
    assert a == b , 'Dict not sorting...'

    
    


def test_init_margin_property(new_value):
    imo = InitialMarginOptimizer(40)
    beg = imo.initial_balance
    #Test get / set
    imo.initial_balance = 0
    assert imo.initial_balance == 0
    
    #Test Exception / Error handling
    #import mymod #-- Not installed? 
    #self.assertRaises(ExpectedException, afunction, arg1, arg2)
    try:
        imo.initial_balance = -50
    except ValueError as e:
        print('Bingo ! Value error caught -- ',e)
        
    #Test revert back to normal, and both public and private methods work.
    imo.initial_balance = beg
    assert imo.initial_balance == beg
    assert imo.init_bal == beg
    
    
    
def test_optimize():
    imo = InitialMarginOptimizer(40)
    print(imo.futures_dict, imo.FUTs)
    assert len(imo.futures_dict) == 10
    
    #Test Optimize Function -- Descending + Intraday symbols
    f, ido = imo.Optimize(['KC','CL'],['NQ'],cushion = 0.1, asc = True)
    print(f,'==',['ES','GC'])
    assert f == ['ES','GC'], 'Optimize Desc Works -- Final Non-ID'
    assert ido == ['NQ'], 'Optimize Desk + ID Works'

    #Test Optimize Function -- Ascending without Intraday
    f, ido = imo.Optimize(['CL','GC','SF'],cushion = 0, asc = False)

    print(f,'==',['NG', 'EC', 'JY', 'KC', 'RTY', 'ES'])
    assert f == ['NG', 'EC', 'JY', 'KC', 'RTY', 'ES'], 'Optimize Asc works...'
    assert ido == []
    
    #Test 
    
    

    
#Testing Functions...
if __name__ == '__main__':

    test_dict_replace_and_add({'NQ':18},('RB',9))
    test_init_margin_property(20)
    test_optimize()

