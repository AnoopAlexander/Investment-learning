# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 16:57:36 2019

@author: anoop
"""

#import openpyxl
import pandas as pd
from configparser import ConfigParser
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def calc_future_cash_flow(value, rate):
    '''
    Find the future cash flow based on value and rate
    '''
    

def main():
    # Get cash flow average for last 4 years
    folder_name = sys.argv[1].split('.')[0]
    cash_flow_df = pd.read_csv(os.path.join(folder_name,'cash_flow_df.csv'))
    balance_sheet_df = pd.read_csv(os.path.join(folder_name,'balance_sheet_df.csv'))
    avg_cash_flow = cash_flow_df['Cash from Operating Activity'][-4:].mean()
    # Provide the growth rate
    growth_rate_1 = int(sys.argv[2])/100
    growth_rate_2 = int(sys.argv[3])/100
    future_cash_flow_list = []
    for i in range(len(cash_flow_df['Cash from Operating Activity'])):
        if i==0:
            future_cash_flow_list.append(avg_cash_flow*(1+growth_rate_1))
        else:
            if i < 5:
                future_cash_flow_list.append(future_cash_flow_list[i-1]*(1+growth_rate_1))
            else:
                future_cash_flow_list.append(future_cash_flow_list[i-1]*(1+growth_rate_2))
    # Find terminal value
    terminal_value = future_cash_flow_list[-1]*((1+ 0.035)/(0.09-0.035))
    # Find present value of future_cash_flow_list
    present_value_list = []
    for i in range(len(future_cash_flow_list)):
        present_value_list.append(future_cash_flow_list[i]/((1+0.09)**(i+1)))
    # Present value of terminal rate
    terminal_present_value = terminal_value/((1+0.09)**10)
    # sum of present values
    sum_present_value = sum(present_value_list) + terminal_present_value
    # Deduct borrowings and cash balance
    net_present_value = sum_present_value - (balance_sheet_df['Borrowings'].iloc[-1]-balance_sheet_df['Cash & Bank'].iloc[-1])
    share_price = net_present_value * 10**7/balance_sheet_df['No. of Equity Shares'].iloc[-1]
    print('share price is {}'.format(share_price))
    
if __name__=="__main__":
    main()
    
    
    
    
    
    