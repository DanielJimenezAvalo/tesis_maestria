import os
import sys
import shutil
import time
import json
from gams import GamsWorkspace

class create_inform_df():

    def __init__(self,runmodel):
        self.runmodel=runmodel

    def print_get_varible(self,variable):

        print('························')
        print(f"{self.runmodel}.out_db.get_variable('{variable}')")
        #print(self.runmodel.out_db.get_variable(f'{variable}').__len__(),"\n")
        
        #if self.runmodel.out_db.get_variable(f'{variable}').__len__() > 1:
        #print(self.runmodel.out_db.get_variable(f'{variable}').__len__())
        self.dict_output={}
        for criteria in ['level','marginal','upper','lower']:
            self.dict_output[criteria]={}
            for rec in self.runmodel.out_db.get_variable(f'{variable}'):
                #print(len(rec.keys))
                if len(rec.keys) != 0:
                    match criteria:
                        case 'level':
                            self.dict_output[criteria][tuple(rec.keys)]= str(rec.level)
                        case 'marginal':
                            self.dict_output[criteria][tuple(rec.keys)]= str(rec.marginal)
                        case 'upper':
                            self.dict_output[criteria][tuple(rec.keys)]= str(rec.upper)
                        case 'lower':
                            self.dict_output[criteria][tuple(rec.keys)]= str(rec.lower)
                else:
                    match criteria:
                        case 'level':
                            self.dict_output[criteria][('1')]= str(rec.level)
                        case 'marginal':
                            self.dict_output[criteria][('1')]= str(rec.marginal)
                        case 'upper':
                            self.dict_output[criteria][('1')]= str(rec.upper)
                        case 'lower':
                            self.dict_output[criteria][('1')]= str(rec.lower)
                
        return self.dict_output

    def print_get_equation(self,equation):

        print('························')
        print(f"{self.runmodel}.out_db.get_equation('{equation}')")
        #print(self.runmodel.out_db.get_equation(f'{equation}').__len__(),"\n")
        
        #if self.runmodel.out_db.get_equation(f'{equation}').__len__() > 1:
        self.dict_output_e={}
        for criteria in ['level','marginal','upper','lower']:
            self.dict_output_e[criteria]={}
            for rec in self.runmodel.out_db.get_equation(f'{equation}'):
                #print(rec.keys)
                #print(tuple(rec.keys))
                if len(rec.keys) !=0:
                    match criteria:
                        case 'level':
                            self.dict_output_e[criteria][tuple(rec.keys)]= str(rec.level)
                        case 'marginal':
                            self.dict_output_e[criteria][tuple(rec.keys)]= str(rec.marginal)
                        case 'upper':
                            self.dict_output_e[criteria][tuple(rec.keys)]= str(rec.upper)
                        case 'lower':
                            self.dict_output_e[criteria][tuple(rec.keys)]= str(rec.lower)
                else:
                    match criteria:
                        case 'level':
                            self.dict_output_e[criteria][('1')]= str(rec.level)
                        case 'marginal':
                            self.dict_output_e[criteria][('1')]= str(rec.marginal)
                        case 'upper':
                            self.dict_output_e[criteria][('1')]= str(rec.upper)
                        case 'lower':
                            self.dict_output_e[criteria][('1')]= str(rec.lower)

        return self.dict_output_e