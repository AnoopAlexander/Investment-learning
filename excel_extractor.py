# python code to extract different data from excel sheet of stock
# Anoop M Alexander
# 30 May 2021

import argparse
import json
import os
import pandas as pd
import sys

def clean_df(df_name):
    '''
    Cleans and converts df to a better format
    '''
    base_df = pd.DataFrame()
    for i in df_name['COMPANY NAME'].values:
        temp_df = df_name[df_name['COMPANY NAME']==i]
        temp_df = temp_df.set_index('COMPANY NAME')
        base_df[i] = temp_df.loc[i].values
    return base_df

def generate_meta_json(df_name):
    '''
    generate the meta json file for the stock
    '''
    print('df is {}'.format(df_name))
    meta_data = {}
    for i in df_name.values:
        print(i)
        meta_data[i[0]] = i[1]
    return meta_data
    
def main():
    '''
    Main function for cleaning
    '''
    base_sheet = pd.ExcelFile(sys.argv[1]).parse('Data Sheet')
    folder_name = sys.argv[1].split('.')[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    print(folder_name)
    meta_df = base_sheet.iloc[4:8]
    profit_loss_df = base_sheet.iloc[14:30]
    balance_sheet_df = base_sheet.iloc[54:69]
    balance_sheet_df = balance_sheet_df.drop_duplicates() 
    cash_flow_df = base_sheet.iloc[80:84]
    master_profit_loss_df = clean_df(profit_loss_df)
    master_balance_sheet_df = clean_df(balance_sheet_df)
    master_cash_flow_df = clean_df(cash_flow_df)
    master_profit_loss_df.to_csv(os.path.join(folder_name,'profit_loss_df.csv'),index=False)
    master_balance_sheet_df.to_csv(os.path.join(folder_name,'balance_sheet_df.csv'),index=False)
    master_cash_flow_df.to_csv(os.path.join(folder_name,'cash_flow_df.csv'),index=False)
    #meta_data = generate_meta_json(meta_df)
    #for i in meta_df.values
    #for i in meta_df.values
    #with open(os.path.join(folder_name,'meta_data.json'),"w") as f:
    #    json.dump(meta_data,f)

print('Starting')
if __name__=="__main__":
    main()