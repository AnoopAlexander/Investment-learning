import os
import sys
import pandas as pd
import plotly.graph_objects as go

def fill_empty_list(df):
    '''
    Fill empty values of the data frame
    '''
    empty_list = df.columns[df.isna().any()].tolist()
    for name in empty_list:
        mean_value = df[name].mean()
        df[name].fillna(value=mean_value,inplace=True)

def main():
    folder_name = sys.argv[1].split('.')[0]
    profit_loss_df = pd.read_csv(os.path.join(folder_name,'profit_loss_df.csv'))
    balance_sheet_df = pd.read_csv(os.path.join(folder_name,'balance_sheet_df.csv'))
    cash_flow_df = pd.read_csv(os.path.join(folder_name,'cash_flow_df.csv'))
    financial_ratio_df = pd.read_csv(os.path.join(folder_name,'financial_ratio_df.csv'))
    fill_empty_list(profit_loss_df)
    fill_empty_list(balance_sheet_df)
    fill_empty_list(cash_flow_df)
    # Plot Revenue and PAT
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=profit_loss_df['Sales'],name="Revenue"))
    fig.add_trace(go.Bar(y=profit_loss_df['Net profit'],name="PAT"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",yaxis_title="Amount Rs cr",title="Revenue PAT ")
    fig.write_html(os.path.join(folder_name,'Revenues_PAT.html'))
    # Plot gross profit margin
    gross_profit = profit_loss_df['Sales'] - (profit_loss_df['Raw Material Cost'] + profit_loss_df['Power and Fuel'] + profit_loss_df['Other Mfr. Exp'])
    gross_profit_margin = gross_profit/profit_loss_df['Sales']
    fig = go.Figure()
    fig.add_trace(go.Bar(y=gross_profit,name="Gross profit"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",yaxis_title="Amount Rs cr",title="Gross Profit")
    fig.write_html(os.path.join(folder_name,'Gross_Profit_Margin.html'))
    # Plot PAT and EPS
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=profit_loss_df['Net profit']*10**7/balance_sheet_df['No. of Equity Shares'],name="EPS"))
    fig.add_trace(go.Bar(y=profit_loss_df['Net profit'],name="PAT"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",yaxis_title="Amount Rs cr",title="EPS PAT ")
    fig.write_html(os.path.join(folder_name,'PAT_and_EPS.html'))
    # Plot Borrowings
    fig = go.Figure()
    fig.add_trace(go.Bar(y=balance_sheet_df['Borrowings'],name="Debt"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",yaxis_title="Amount Rs cr",title="Debt")
    fig.write_html(os.path.join(folder_name,'Debt.html'))
    # Plot Debt to ebit
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=balance_sheet_df['Borrowings']/financial_ratio_df['ebit'],name="Debt to Ebit"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",yaxis_title="debt_to_ebit",title="Debt to Ebit")
    fig.write_html(os.path.join(folder_name,'Debt_to_ebit.html'))
    # Plot Debt to Equity
    fig = go.Figure()
    fig.add_trace(go.Bar(y=financial_ratio_df['debt_to_equity'],name="Debt to Equity"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",yaxis_title="debt_to_equity",title="Debt to Equity")
    fig.write_html(os.path.join(folder_name,'Debt_to_equity.html'))
    # Plot PAT to inventory
    fig = go.Figure()
    fig.add_trace(go.Bar(y=profit_loss_df['Net profit'],name="PAT"))
    fig.add_trace(go.Scatter(y=balance_sheet_df['Inventory'],name="Inventory"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",title="PAT and Inventory")
    fig.write_html(os.path.join(folder_name,'PAT_and_Inventory.html'))
    # Plot Inventory days
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=financial_ratio_df['inventory_days'],name="Inventory days"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",title="Inventory days")
    fig.write_html(os.path.join(folder_name,'Inventory_days.html'))
    # Plot receivables to sales ratio
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=1/financial_ratio_df['account_receivables_turnover'],name="Receivables to sales"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",title="Receivables_to_sales")
    fig.write_html(os.path.join(folder_name,'Receivables_to_sales.html'))
    # Plot cash flow from operations
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=cash_flow_df['Cash from Operating Activity'],name="Cash flow"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",title="Cash flow")
    fig.write_html(os.path.join(folder_name,'Cash_flow.html'))
    # Plot Return on equity
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=financial_ratio_df['return_on_equity'],name="ROE"))
    fig.update_layout(hovermode="x unified",xaxis_title="Year",title="ROE")
    fig.write_html(os.path.join(folder_name,'ROE.html'))
    
if __name__=="__main__":
    main()
    