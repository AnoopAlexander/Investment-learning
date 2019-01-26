# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 17:35:07 2018

@author: anoop
"""

#import os
#import matplotlib.pyplot as plt
import pandas as pd
from configparser import ConfigParser
import matplotlib.pyplot as plt 
import numpy as np


parser = ConfigParser()
parser.read('config/MothersonSumi.ini')
face_value = float(parser.get('financials','face_value'))
current_share_price = float(parser.get('financials','current_share_price'))
number_of_shares = float(parser.get('financials','number_of_shares'))
total_expense = np.array((parser.get('financials','total_expense').split(' '))).astype(np.float)
#print(total_expense)
working_capital = np.array((parser.get('financials','working_capital').split(' '))).astype(np.float)
finance_cost = np.array((parser.get('financials','finance_cost').split(' '))).astype(np.float)
depreciation = np.array((parser.get('financials','depreciation').split(' '))).astype(np.float)
sales_revenue = np.array((parser.get('financials','sales_revenue').split(' '))).astype(np.float)
other_income = np.array((parser.get('financials','other_income').split(' '))).astype(np.float)
cost_of_making_goods = np.array((parser.get('financials','cost_of_goods_sold').split(' '))).astype(np.float)
receivables = np.array((parser.get('financials','receivables').split(' '))).astype(np.float)
profit_before_tax = np.array((parser.get('financials','pbt').split(' '))).astype(np.float)
profit_after_tax = np.array((parser.get('financials','pat').split(' '))).astype(np.float)
borrowings = np.array((parser.get('financials','borrowings').split(' '))).astype(np.float)
inventories = np.array((parser.get('financials','inventories').split(' '))).astype(np.float)
assets = np.array((parser.get('financials','assets').split(' '))).astype(np.float)
share_capital = np.array((parser.get('financials','share_capital').split(' '))).astype(np.float)
reserves = np.array((parser.get('financials','reserves').split(' '))).astype(np.float)
cash_flow_opertaing_activity = np.array((parser.get('financials','cash_flow_operating_activity').split(' '))).astype(np.float)
assets_purchased = np.array((parser.get('financials','assets_purchased').split(' '))).astype(np.float)
assets_sold = np.array((parser.get('financials','assets_sold').split(' '))).astype(np.float)
tax = np.array((parser.get('financials','tax').split(' '))).astype(np.float)
eps = np.array((parser.get('financials','eps').split(' '))).astype(np.float)

gross_profit = np.zeros(sales_revenue.shape)
gpm = np.zeros(gross_profit.shape)
operating_expense = np.zeros(total_expense.shape)
ebitda = np.zeros(sales_revenue.shape)
ebit = np.zeros(ebitda.shape)
ebitda_margin = np.zeros(ebitda.shape)
pat_margin = np.zeros(sales_revenue.shape)
shareholder_equity = np.zeros(reserves.shape)
financial_leverage = np.zeros(reserves.shape)
roe = np.zeros(financial_leverage.shape)
roa = np.zeros(finance_cost.shape)
pbit = np.zeros(profit_before_tax.shape)
oce = np.zeros(borrowings.shape)
roce = np.zeros(finance_cost.shape)
interest_coverage_ratio = np.zeros(finance_cost.shape)
financial_leverage_ratio = np.zeros(assets.shape)
asset_turnover = np.zeros(sales_revenue.shape)
inventory_turnover = np.zeros(inventories.shape)
inventory_no_of_days = np.zeros(inventories.shape)
receivables_turnover_ratio = np.zeros(sales_revenue.shape)
average_collection_time = np.zeros(receivables_turnover_ratio.shape)
total_revenue = np.zeros(sales_revenue.shape)
free_cash_flow = np.zeros(cash_flow_opertaing_activity.shape)
debt_to_equity_ratio = np.zeros(shareholder_equity.shape)
debt_to_pbt_ratio = np.zeros(borrowings.shape)
sales_to_receivables_ratio = np.zeros(sales_revenue.shape)
net_cash_flow = np.zeros(cash_flow_opertaing_activity.shape)
#average_inventory = np.zeros(inventories.shape)
#average_inventory = np.insert(average_inventory,0,0)
#average_inventory = np.insert(average_inventory,-1,0)

#print('now gross profit is ',gross_profit)
# find gross profit

working_capital_turnover = sales_revenue[-1]/np.mean(working_capital[-2:])

for i in range(len(sales_revenue)):
    gp = sales_revenue[i] - cost_of_making_goods[i]
    gross_profit[i] += gp
    
for i in range(len(gross_profit)):
    gpm[i] = gross_profit[i]/sales_revenue[i]
    
for i in range(len(operating_expense)):
    operating_expense[i] = total_expense[i] - depreciation[i] - finance_cost[i]
    
for i in range(len(ebitda)):
    ebitda[i] = sales_revenue[i] - operating_expense[i]

for i in range(len(ebit)):
    ebit[i] = ebitda[i] - depreciation[i]
    
for i in range(len(ebitda_margin)):
    ebitda_margin[i] =  ebitda[i]/sales_revenue[i]

for i in range(len(total_revenue)):
    total_revenue[i] = sales_revenue[i] + other_income[i]
    pat_margin[i] = (profit_after_tax[i]/total_revenue[i])*100
    
for i in range(len(asset_turnover)):
    asset_turnover[i] = sales_revenue[i]/assets[i]

for i in range(len(financial_leverage)):
    shareholder_equity[i] = share_capital[i] + reserves[i]
    financial_leverage[i] = assets[i]/shareholder_equity[i]

for i in range(len(roe)):
    roe[i] = pat_margin[i]*asset_turnover[i]*financial_leverage[i]

for i in range(len(inventory_turnover)):
    inventory_turnover[i] = cost_of_making_goods[i]/inventories[i]
    inventory_no_of_days[i] = 365/inventory_turnover[i]
    
for i in range(len(receivables_turnover_ratio)):
    receivables_turnover_ratio[i] = sales_revenue[i]/receivables[i]
    average_collection_time[i] = 365/receivables_turnover_ratio[i]
    
for i in range(len(free_cash_flow)):
    free_cash_flow[i] = cash_flow_opertaing_activity[i] + assets_sold[i] - assets_purchased[i]

for i in range(len(roa)):
    interest = (1 - tax[i])
    interest = finance_cost[i]*interest
    roa_numerator = profit_after_tax[i] + interest
    roa[i] = roa_numerator/assets[i]
    
for i in range(len(roce)):
    pbit[i] = profit_before_tax[i] + finance_cost[i]
    oce[i] = borrowings[i] + shareholder_equity[i]
    roce[i] = pbit[i]/oce[i]
    
for i in range(len(interest_coverage_ratio)):
    interest_coverage_ratio[i] = ebit[i]/finance_cost[i]
    
for i in range(len(debt_to_equity_ratio)):
    debt_to_equity_ratio[i] = borrowings[i]/shareholder_equity[i]
    
for i in range(len(financial_leverage_ratio)):
    financial_leverage_ratio[i]=assets[i]/shareholder_equity[i]

for i in range(len(debt_to_pbt_ratio)):
    debt_to_pbt_ratio[i] = (borrowings[i]/profit_before_tax[i])*100

for i in range(len(sales_revenue)):
    sales_to_receivables_ratio[i] = (receivables[i]/sales_revenue[i])*100

for i in range(len(cash_flow_opertaing_activity)):
    net_cash_flow[i] = cash_flow_opertaing_activity[i] - assets_purchased[i]        
#number_of_shares = share_capital[-1]/face_value
sales_per_share = sales_revenue[-1]/number_of_shares
price_to_sales = current_share_price/sales_per_share
book_value = (share_capital[-1]+reserves[-1])/number_of_shares
price_to_book_value = current_share_price/book_value
earnings_per_share = profit_after_tax[-1]/number_of_shares
price_to_earnings = current_share_price/earnings_per_share
cagr_dataframe = pd.DataFrame(columns=['revenue','pat'])
cash_flow_average = np.sum(net_cash_flow[-1:-5])/len(net_cash_flow[-1:-5])
#graph plots
#sales revenue and pat
revenue_pc_change = pd.Series(sales_revenue)
revenue_pc_change.name = 'revenues'
pat_pc_change = pd.Series(profit_after_tax)
pat_pc_change.name = 'PAT'
pct_dataframe = pd.concat([revenue_pc_change,pat_pc_change,revenue_pc_change.pct_change(),pat_pc_change.pct_change()],axis=1)
pct_dataframe['debt_to_profit'] = pd.Series(debt_to_pbt_ratio)
revenue_cagr = ((sales_revenue[-1]/sales_revenue[0])**(1/len(sales_revenue)))-1.0
pat_cagr = ((profit_after_tax[-1]/profit_after_tax[0])**(1/len(profit_after_tax))) - 1.0
eps_cagr = ((eps[-1]/eps[0])**(1/len(eps))) - 1.0
cagr_dataframe = cagr_dataframe.append({'revenue':revenue_cagr,'pat':pat_cagr,'eps':eps_cagr},ignore_index=True)
time_in_years = np.arange(0,12,1)
#revenues pat
fig,axis = plt.subplots()
axis.plot(time_in_years,sales_revenue,'o-')
axis2=axis.twinx()
axis2.plot(time_in_years,profit_after_tax,'x-',color='red')
axis.set_xticks(time_in_years)
axis.set(xlabel='time_years',ylabel='revenue',title='revenue_pat_YOY')
axis2.set(ylabel='PAT')
fig.savefig('/Investment/plots/motherson_sumi/revenue.png')

#eps and pat evaluation
fig,axis = plt.subplots()
axis.plot(time_in_years,profit_after_tax,'o-')
axis.set_xticks(time_in_years)
axis2 = axis.twinx()
axis2.plot(time_in_years,eps,'x-',color='red')
axis.set(xlabel='time_years',ylabel='PAT',title='pat_eps_YOY')
axis2.set(ylabel='EPS_YOY')
fig.savefig('/Investment/plots/motherson_sumi/eps.png')
#gross profit margin
fig,axis = plt.subplots()
axis.plot(time_in_years,gpm,'o-')
axis.set_xticks(time_in_years)
axis.set(xlabel='time_years',ylabel='gpm',title='gpm_YOY')
fig.savefig('/Investment/plots/motherson_sumi/gpm.png')
#debt and earnings bbefore tax
fig,(axis1,axis2,axis3) = plt.subplots(3,sharex=True)
axis1.plot(time_in_years,borrowings,'o-')
axis1.set_xticks(time_in_years)
axis1.set(xlabel='time_years',ylabel='borrowings',title='borrowings_YOY')
axis2.plot(time_in_years,profit_before_tax,'x-')
axis2.set(ylabel='pbit')
axis3.plot(time_in_years,debt_to_pbt_ratio,'*-')
axis3.set(ylabel='debt_to_pbit')
fig.savefig('/Investment/plots/motherson_sumi/debt_to_profit.png')
#inventory pat and inventory days check
fig,(axis1,axis2,axis3)=plt.subplots(3,sharex=True)
axis1.plot(time_in_years,inventories,'o-')
axis1.set_xticks(time_in_years)
axis1.set(ylabel='inventories')
axis2.plot(time_in_years,profit_after_tax,'x-')
axis2.set(ylabel='PAT')
axis3.plot(time_in_years,inventory_no_of_days,'*-')
axis3.set(ylabel='inventory_days')
fig.savefig('/Investment/plots/motherson_sumi/inventory_PAT.png')
#sales to receivables
fig,(axis1,axis2) = plt.subplots(2,sharex=True)
axis1.plot(time_in_years,sales_revenue,'o-')
axis1.set_xticks(time_in_years)
axis1.set(ylabel='sales_revenue')
axis2.plot(time_in_years,receivables,'x-')
axis2.set(ylabel='receivables')
fig.savefig('/Investment/plots/motherson_sumi/sales_receivables.png')
fig,axis = plt.subplots()
axis.plot(time_in_years,sales_to_receivables_ratio,color='red')
axis.set_xticks(time_in_years)
axis.set(xlabel='time_years',ylabel='receivables',title='receivables_sales_pct')
fig.savefig('/Investment/plots/motherson_sumi/receivables_sales.png')
#cash flow operations
fig,axis = plt.subplots()
axis.plot(time_in_years,cash_flow_opertaing_activity,'o-')
axis.set_xticks(time_in_years)
axis.set(xlabel='time_years',ylabel='cash flow',title='Cash flow YOY')
fig.savefig('/Investment/plots/motherson_sumi/cash_flow_operations.png')
#pat and shareholders equity
fig,axis=plt.subplots()
axis.plot(time_in_years,roe,'o-')
axis.set_xticks(time_in_years)
axis.set(xlabel='time_years',ylabel='roe')
fig.savefig('/Investment/plots/motherson_sumi/roe.png')
# net cash flow
fig,axis = plt.subplots()
axis.plot(time_in_years,net_cash_flow,'o-')
axis.set_xticks(time_in_years)
axis.set(xlabel='time_years',ylabel='net_cash_flow',title='net_cash_flow_YOY')
fig.savefig('/Investment/plots/motherson_sumi/net_cash_flow.png')
print('Average_cash_flow ',cash_flow_average)
#print(debt_to_pbt_ratio)
#print(revenue_pc_change.pct_change())
#print(pat_pc_change.pct_change())
#print(pct_dataframe)
#print(revenue_cagr)
#print(pat_cagr)
#print(cagr_dataframe)
#print(sales_revenue)
#print(earnings_per_share)
#print(price_to_earnings)
#print(price_to_sales)
#print(price_to_book_value)    
#print(working_capital_turnover)
#print(number_of_shares)
# =============================================================================
# print(gross_profit)
# print(gpm)
# print(operating_expense)
# print(ebitda)
#print(ebit)
# print(ebitda_margin)
# =============================================================================
#print(inventory_turnover)
#print(inventory_no_of_days)
# =============================================================================
#print(roa)
# =============================================================================
# print(shareholder_equity)
# print(pbit)
# print(oce)
#print(roce)
# =============================================================================
#print(interest_coverage_ratio)
#print(debt_to_equity_ratio)
#print(financial_leverage_ratio)
#print(receivables_turnover_ratio)
#print(average_collection_time)