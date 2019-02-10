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

class Fundamental_Analysis:
    def __init__(self,file):
        """
        The basic initialisation class which would initialise the various
        variables. Currently the excel file to be parsed is read. There 
        would be more added.
        """
        self.basefile = file 
        self.time_axis = []
        self.feature_list = []
        self.dataframe = pd.DataFrame()
        self.cagrdataframe = pd.DataFrame()
    
    def getDataFrame(self):
        """
        The function is used to get the data frames from the excel sheet
        which we feed as input argument. Pandas is used to parse the 
        excel sheet into different dataframes.
        
        Input: Base file initialised which our base excel file
        
        return: 3 data frames of balance sheet, profit_loss and cash flow.
        """
        excel_file = pd.ExcelFile(self.basefile)
        #print(excel_file.sheet_names)
        df_balance_sheet = excel_file.parse('Balance Sheet')
        df_profit_loss = excel_file.parse('Profit & Loss')
        df_cash_flow = excel_file.parse('Cash Flow')
        df_data_sheet = excel_file.parse('Data Sheet')
        return df_balance_sheet,df_profit_loss,df_cash_flow,df_data_sheet
    
    def cleanDataFrame(self,dataframe,name):
        """
        This function was created to clean and format the dataframe. The
        dataframe is assigned a new index from a given column and also the 
        values showing NaN are dropped.
        
        Inputs: dataframe which has to be cleaned,name of the index to set 
                as columns
                
        return: a cleaned and formatted version of the dataframe
        """
        dataframe.set_index(name,inplace=True)
        dataframe.dropna(inplace=True)
        return dataframe
    
    def getSeriesfromData(self,dataframe,index_name,pruning_number=0):
        """
        This function is created to get the data of a specific index in a
        dataframe as a series. the series is also cleared to get specific 
        values for the time period
        
        Inputs: dataframe to search, the name of the row to convert as series
        number of rows to cut out
        
        return: series of the specified index from the table
        
        Additionally adds the feature in analysis into the feature list
        
         """
        series = dataframe.loc[index_name]
        if pruning_number < 0:
            series = series[:pruning_number]
        #self.feature_list.append(series)
        return series
    
    def addSeriestoList(self,series):
        """
        This function is created to add series to the feature list which is used
        to plot graphs.
        
        Input: Series which needs to be appended
        
        Adds the series to the feature list
        """
        self.feature_list.append(series)
    
    def plotGraph(self,nrows,ncols,feature_list,title,save_path,singleplot=False):
        """
        This function is used to create subplots of the given features.
        
        Input: no of rows in the subplot, no of columns in the subplot,
        list of features to plot
        
        No return only plot of the graph is saved
        
        """
        ext = '.png'
        if singleplot:
            plt.plot(self.time_axis,feature_list[0],'-o')
            plt.savefig(os.path.join(save_path+title+ext))
        else:
            fig,axes = plt.subplots(nrows,ncols,sharex=True)
            for idx,feature in enumerate(feature_list):
                axes[idx].plot(self.time_axis,feature,'-o')
            fig.savefig(os.path.join(save_path+title+ext))
        feature_list.clear()
        
    def addTodataframe(self,heading,value):
        """
        This function is used to add columns to a dataframe. Currently used to 
        add the percentage change into the dataframe
        
        Input: the heading name for the series, values which need to be added
        as columns
        
        No return only modification of the initialised dataframe.
        """
        value.name = heading
        self.dataframe = pd.concat([value],axis=1)

    def dataFrameasexcel(self,path,name):
        """
        This function saves the dataframe to a given path.
        Input: the path to where the dataframe needs to be saved, name of the
        excel file to be saved.
        
        No return only saves as excel files.
        """
        #print(os.path.join(path,name,'.xlsx'))
        if name=='pct_change':
            self.dataframe.to_excel(os.path.join(path,name +'.xlsx'))           
        else:
            self.cagrdataframe.to_excel(os.path.join(path,name +'.xlsx'))
    
    def getCagr(self,heading,series):
        """
        This function is used to calculate the CAGR of a given series.
        
        Input: series for which cagr is to be calculated
        
        No return only add cagr to the cagr dataframe
        """
        cagr = ((series[-1]/series[0])**(1/len(series)))-1.0
        cagr_series = pd.Series(cagr)
        cagr_series.name = heading
        self.cagrdataframe = pd.concat([cagr_series],axis=1)
        #return cagr

parser = ConfigParser()
parser.read('config/MothersonSumi.ini')
save_place = parser.get('main','save_path')
base_stock = Fundamental_Analysis(parser.get('main','name'))
balance_sheet,profit_loss,cash_flow,data_sheet = base_stock.getDataFrame()
balance_sheet = base_stock.cleanDataFrame(balance_sheet,parser.get('main','index_name'))
profit_loss = base_stock.cleanDataFrame(profit_loss,parser.get('main','index_name'))
cash_flow = base_stock.cleanDataFrame(cash_flow,parser.get('main','index_name'))
data_sheet = base_stock.cleanDataFrame(data_sheet,parser.get('data_sheet','index_name'))
#print(data_sheet)
#revenue and profit_after_tax
revenues = np.array(base_stock.getSeriesfromData(profit_loss,'Sales',-3))
profit_after_tax = np.array(base_stock.getSeriesfromData(profit_loss,'Net profit',-3))
base_stock.addSeriestoList(revenues)
base_stock.addSeriestoList(profit_after_tax)
revenues_cagr = base_stock.getCagr('revenue_cagr',revenues)
base_stock.time_axis = np.arange(1,len(revenues)+1,1)
base_stock.plotGraph(2,1,base_stock.feature_list,'Revenue_PAT_YOY',save_place)
base_stock.addTodataframe('revenues_pct',pd.Series(revenues).pct_change())

# eps and share capital
eps = np.array(base_stock.getSeriesfromData(profit_loss,'EPS',-3))
share_captial = np.array(base_stock.getSeriesfromData(balance_sheet,'Equity Share Capital'))
base_stock.addSeriestoList(eps)
base_stock.addSeriestoList(share_captial)
base_stock.addTodataframe('eps_pct',pd.Series(eps).pct_change())
base_stock.plotGraph(2,1,base_stock.feature_list,'Eps_Share_capital_YOY',save_place)

#Gross profit margin
print(base_stock.feature_list)
sales = np.array(base_stock.getSeriesfromData(data_sheet,'Sales'))
sales =sales[0,]
raw_material_cost = np.array(base_stock.getSeriesfromData(data_sheet,'Raw Material Cost'))
power_fuel = np.array(base_stock.getSeriesfromData(data_sheet,'Power and Fuel'))
manufacture_cost = np.array(base_stock.getSeriesfromData(data_sheet,'Other Mfr. Exp'))
cost_of_goods_sold = raw_material_cost + power_fuel + manufacture_cost
gross_profit_margin = (sales - cost_of_goods_sold)/sales
base_stock.addSeriestoList(gross_profit_margin)
print(base_stock.feature_list)
base_stock.plotGraph(0,0,base_stock.feature_list,'GPM_YOY',save_place,True)

base_stock.dataFrameasexcel(parser.get('main','excel_path'),'pct_change')
base_stock.dataFrameasexcel(parser.get('main','excel_path'),'cagr')
#plt.plot(base_stock.time_axis,gross_profit_margin)
#print(base_stock.feature_list[0])
#print(cost_of_goods_sold)
#print(raw_material_cost)
#print(sales)
#print(balance_sheet.loc['Equity Share Capital'])
#print(eps)
#print(share_captial)
#print(base_stock.dataframe)
#print(pd.Series(revenues).pct_change())
#print(base_stock.dataframe)
#print('base stock time is ',base_stock.time_axis)
# =============================================================================
# print('revenues is ',revenues)
# print('profit after tax is ',profit_after_tax)
# print('shape of revenues is ',revenues.shape)
# print('shape of profit after tax is ',profit_after_tax.shape)
# print('shape of base_stock is ',base_stock.time_axis.shape)
# print('type of revenues is ',type(revenues))
# print('type of profit after tax is ',type(profit_after_tax))
# print('type of base_stock time is ',type(base_stock.time_axis))
# 
# =============================================================================
#for idx,features in enumerate(base_stock.feature_list):
#    print(idx,features)
    
#base_stock.feature_list.clear()
#print(base_stock.feature_list)
#fig,axis = plt.subplots(2,1,sharex=True) 
#axis[0].plot(base_stock.time_axis,base_stock.feature_list[0],'-o')
#axis[1].plot(base_stock.time_axis,profit_after_tax,'-o')
#print(profit_after_tax)
#print(revenues_cagr)
#balance_sheet.set_index(parser.get('main','index_name'),inplace=True)
#balance_sheet.dropna(inplace=True)
#columns = balance_sheet.loc['Narration'].tolist()
#print(columns)
#print(balance_sheet)
#print(profit_loss)
#print(cash_flow)