#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:05:24 2020

@author: zoakes
"""

class InitialMarginOptimizer:
    
    '''TRY CHANGING TO SELF._FUTS (private) -- Consider adding cushion ?'''
    def __init__(self,initial_balance_thousands, futures_dict=None):
        self.init_bal = initial_balance_thousands
        if futures_dict is None:
            self.FUTs = {'NQ':16.5, 'ES':13.2,'GC':9,'RTY':6.38,'CL':7.5,'KC':4.5, 'SF':4.4,'JY':4, 'EC':2.5,'NG':2.2}
        else:
            self.FUTs = futures_dict
        #self.futures_dict = 0
        self.final = []
        self.intraday = []
        print(f'Initial Margin Optimizer Initialized -- Initial Balance -- {self.init_bal} \nFutures Dict -- {self.FUTs}')         
    
    @property      
    def futures_dict(self):
        return self.FUTs
    
    @futures_dict.setter
    def futures_dict(self,new):
        assert isinstance(new, tuple) or isinstance(new, dict)
        if isinstance(new, tuple) and len(new) == 2:
            self.FUTs[new[0]] = new[1]
        else:
            self.FUTs = new
        #tmp = sorted(self.FUTs.items(), key=lambda x: x[1], reverse=True)
        tmp = {}
        #Alot of effort -- maybe easier to use list of tuples?
        self.FUTs = {k:v for k,v in sorted(self.FUTs.items(), key=lambda x: x[1], reverse=True)}
        
            
    @property
    def initial_balance(self):
        return self.init_bal
    
    @initial_balance.setter
    def initial_balance(self, new_bal):
        if new_bal < 0:
            raise ValueError("inital balance < 0 is not possible.")
        self.init_bal = new_bal
    
        
    def Optimize(self, sym_skip = [], intraday_only = [], cushion = .1, asc = False, idx_skip = 0):
        balance = self.init_bal
        min_bal = self.init_bal * cushion if cushion > 0 else 0
        final, ID = [], []
        for sym, val in sorted(list(self.FUTs.items()), key=lambda x: x[1], reverse=asc)[idx_skip:]:
            if sym in sym_skip:
                continue
            if sym in intraday_only: #Intraday Margin -- 50% Discount
                print(sym, val)
                val *= .5
                print(sym, val)
            if balance - val > min_bal:
                if sym in intraday_only:
                    print(sym, val)
                    balance -= val
                    ID.append(sym)
                else:
                    balance -= val
                    final.append(sym)
            else:
                print(f'min margin met... {balance}')
                break

        print(f'$ Used  -- {self.init_bal - balance}')
        if balance - min_bal != balance:
            print(f'$ Excess Cushion -- {balance - min_bal}') #Excess Cushion
        print(f'$ Total Cushion -- {balance}')
        print(f'Final Symbols -- {final}')
        
        self.intraday = ID
        self.final = final
        return self.final, self.intraday
                
        

if __name__ == '__main__':
    #FUTs = {'NQ':16.5, 'ES':13.2,'GC':9,'RTY':6.38,'CL':7.5,'KC':4.5, 'SF':4.4,'JY':4, 'EC':2.5,'NG':2.2}
    imo = InitialMarginOptimizer(39)
    
    imo.Optimize(['KC','CL'],['NQ'],cushion = 0.1, asc = True)
    
    