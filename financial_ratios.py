# python code to calculate financial ratios of a stock
# Anoop M Alexander
# 06 June 2021

import argparse
import os
import pandas as pd
import sys

def fill_empty_list(df):
    '''
    Fill empty values of the data frame
    '''
    empty_list = df.columns[df.isna().any()].tolist()
    for name in empty_list:
        mean_value = df[name].mean()
        df[name].fillna(value=mean_value,inplace=True)

def main():
    '''
    Main function to execute
    '''
    financial_ratio_df = pd.DataFrame()
    folder_name = sys.argv[1].split('.')[0]
    profit_loss_df = pd.read_csv(os.path.join(folder_name,'profit_loss_df.csv'))
    balance_sheet_df = pd.read_csv(os.path.join(folder_name,'balance_sheet_df.csv'))
    cash_flow_df = pd.read_csv(os.path.join(folder_name,'cash_flow_df.csv'))
    fill_empty_list(profit_loss_df)
    fill_empty_list(balance_sheet_df)
    fill_empty_list(cash_flow_df)
    operating_income = profit_loss_df['Sales'] - profit_loss_df['Other Income']
    total_expense = (profit_loss_df['Raw Material Cost'] + profit_loss_df['Power and Fuel'] +
                    profit_loss_df['Other Mfr. Exp'] + profit_loss_df['Employee Cost'] +
                    profit_loss_df['Selling and admin'] + profit_loss_df['Other Expenses'])
    operating_expense = total_expense - profit_loss_df['Depreciation'] - balance_sheet_df['Borrowings']
    ebidta = operating_income - operating_expense
    ebidta_margin = ebidta/profit_loss_df['Sales']
    pat_margin = profit_loss_df['Net profit']/(profit_loss_df['Sales']+profit_loss_df['Other Income'])
    asset_turnover = profit_loss_df['Sales']/balance_sheet_df['Total']
    financial_leverage = balance_sheet_df['Total']/(balance_sheet_df['Equity Share Capital'] + 
                         balance_sheet_df['Reserves'])
    return_on_equity = pat_margin*asset_turnover*financial_leverage
    return_on_asset = (profit_loss_df['Net profit'] + profit_loss_df['Interest']*(1-0.3))/balance_sheet_df['Total']
    overall_capital = (balance_sheet_df['Borrowings'] + balance_sheet_df['Reserves'] +
                      balance_sheet_df['Equity Share Capital'])
    return_on_capital = profit_loss_df['Profit before tax']/overall_capital
    ebit = ebidta - profit_loss_df['Depreciation']
    interest_coverage_ratio = ebit/profit_loss_df['Interest']
    debt_to_equity = balance_sheet_df['Borrowings']/(balance_sheet_df['Equity Share Capital'] + 
                     balance_sheet_df['Reserves'])
    debt_to_asset = balance_sheet_df['Borrowings']/balance_sheet_df['Total']
    fixed_asset_turnover = profit_loss_df['Sales']/balance_sheet_df['Total']
    inventory_turnover = (profit_loss_df['Raw Material Cost'] + profit_loss_df['Power and Fuel'] + 
                          profit_loss_df['Other Mfr. Exp'])/balance_sheet_df['Inventory']
    inventory_days = 365/inventory_turnover
    account_receivables_turnover = profit_loss_df['Sales']/balance_sheet_df['Receivables']
    days_sales_outstanding = 365/account_receivables_turnover
    working_capital = balance_sheet_df['Other Assets'] - balance_sheet_df['Other Liabilities']
    working_capital_turnover = profit_loss_df['Sales']/working_capital
    financial_ratio_df['operating_income'] = operating_income
    financial_ratio_df['total_expense'] = total_expense
    financial_ratio_df['operating_expense'] = operating_expense
    financial_ratio_df['ebidta'] = ebidta
    financial_ratio_df['ebidta_margin'] = ebidta_margin
    financial_ratio_df['pat_margin'] = pat_margin
    financial_ratio_df['asset_turnover'] = asset_turnover
    financial_ratio_df['financial_leverage'] = financial_leverage
    financial_ratio_df['return_on_equity'] = return_on_equity
    financial_ratio_df['return_on_asset'] = return_on_asset
    financial_ratio_df['overall_capital'] = overall_capital
    financial_ratio_df['return_on_capital'] = return_on_capital
    financial_ratio_df['ebit'] = ebit
    financial_ratio_df['interest_coverage_ratio'] = interest_coverage_ratio
    financial_ratio_df['debt_to_equity'] = debt_to_equity
    financial_ratio_df['debt_to_asset'] = debt_to_asset
    financial_ratio_df['fixed_asset_turnover'] = fixed_asset_turnover
    financial_ratio_df['inventory_turnover'] = inventory_turnover
    financial_ratio_df['inventory_days'] = inventory_days
    financial_ratio_df['account_receivables_turnover'] = account_receivables_turnover
    financial_ratio_df['days_sales_outstanding'] = days_sales_outstanding
    financial_ratio_df['working_capital'] = working_capital
    financial_ratio_df['working_capital_turnover'] = working_capital_turnover
    financial_ratio_df.to_csv(os.path.join(folder_name,'financial_ratio_df.csv'),index=False)

if __name__=="__main__":
    main()