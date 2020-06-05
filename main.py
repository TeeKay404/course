import csv
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import matplotlib.dates as mdates
import datetime

def get_profit(i):
    ### Считаем доход в процентах по формулам
    if (df_Result.type[i] == 'BUY'):
        df_Result.loc[i, 'DiffPercentage'] = (df_Result.priceClosed[i]/df_Result.priceOpen[i]-1)*100
    elif (df_Result.type[i] == 'SELL'):
        df_Result.loc[i, 'DiffPercentage'] = (df_Result.priceOpen[i]/df_Result.priceClosed[i]-1)*100
    ### Суммируем процент дохода
    if (i>0):
        df_Result.loc[i, 'profit'] = df_Result.profit[i-1] + df_Result.DiffPercentage[i]
    else:
        df_Result.loc[i, 'profit'] = df_Result.loc[i, 'DiffPercentage']

def graph():
    ###визуализация графика профита
    df_Result.reset_index().plot(x='index', y='profit')
    plt.show()

def save(file_csv):
    ### сохранить файл
    file_csv.to_csv (r'D:\Atom python\python projects\analysis\result.csv', index = False, header=True)

def show_buy_and_sell_in_hour(date_start, date_end, format='H'):
    ### Вывести количество buy и sell за период времени за каждый час
    orders_Date = df_Traders[(df_Traders['date_Open'] >= date_start)&(df_Traders['date_Open'] <= date_end)]
    orders_Date['date_Open'] = orders_Date['date_Open'].dt.ceil(format)
    orders_Date.groupby([orders_Date["date_Open"], "trade_Type"]).size().to_frame("trade_Type")["trade_Type"].unstack().plot.bar(rot=45, grid=True)
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize=5)
    plt.show()

def get_count_buy_and_sell(date_start, date_end):
    ### Возвращает количество buy и sell за период времени
    orders_BUY = df_Traders[(df_Traders['date_Open'] >= date_start) & (df_Traders['date_Open'] <= date_end) & (df_Traders['trade_Type'] == "BUY") ]
    orders_SELL = df_Traders[(df_Traders['date_Open'] >= date_start) & (df_Traders['date_Open'] <= date_end) & (df_Traders['trade_Type'] == "SELL") ]
    quantity_orders_BUY=len(orders_BUY.index)
    quantity_orders_SELL=len(orders_SELL.index)
    return(quantity_orders_BUY, quantity_orders_SELL)

def main_function(date_start, date_end, period_value, interval_value, actionTime_value):
    startTime = date_start
    period = datetime.timedelta(minutes = period_value) # каждые [period_value] минут выполняем функцию
    interval = datetime.timedelta(minutes = interval_value) # интервал просматриваемого времени
    actionTime = datetime.timedelta(minutes = actionTime_value) # время действия сделки или через сколько закрывать сделку
    i = 0
    while (startTime < date_end):
        BUY, SELL = get_count_buy_and_sell(startTime, startTime+interval)
        if (BUY > SELL):
            df_Result.loc[i, 'type'] = 'BUY'
            df_Result.loc[i, 'dateOpen'] =  startTime+interval
            df_Result.loc[i, 'dateClosed'] = startTime+interval+actionTime
            df_Result.loc[i, 'priceOpen'] = df_FXEURUSD.loc[df_FXEURUSD['date'] == startTime+interval]['open'].item()
            df_Result.loc[i, 'priceClosed'] = df_FXEURUSD.loc[df_FXEURUSD['date'] == startTime+interval+actionTime]['close'].item()
            df_Result.loc[i, 'DiffPercentage'] = None
            df_Result.loc[i, 'profit'] = None
            get_profit(i)
            i=i+1
        elif(SELL>BUY):
            df_Result.loc[i, 'type'] = 'SELL'
            df_Result.loc[i, 'dateOpen'] =  startTime+interval
            df_Result.loc[i, 'dateClosed'] = startTime+interval+actionTime
            df_Result.loc[i, 'priceOpen'] = df_FXEURUSD.loc[df_FXEURUSD['date'] == startTime+interval]['open'].item()
            df_Result.loc[i, 'priceClosed'] =  df_FXEURUSD.loc[df_FXEURUSD['date'] == startTime+interval+actionTime]['close'].item()
            df_Result.loc[i, 'DiffPercentage'] = None
            df_Result.loc[i, 'profit'] = None
            get_profit(i)
            i=i+1
        startTime = startTime+period
    result = df_Result.profit[-1:]
    print('Сумма всех доходов в процентах = ', df_Result.profit[-1:])
    save(df_Result)
    graph()


#############              main                 ################
df_Traders = pd.read_csv('traders.csv', header = 0, sep= ';')
df_Traders['date_Open'] = pd.to_datetime(df_Traders['date_Open'], format = '%Y/%m/%d %H:%M:%S')
df_Traders['date_Closed'] = pd.to_datetime(df_Traders['date_Closed'], format = '%Y/%m/%d %H:%M:%S')
df_Result = pd.DataFrame({'type':[],'dateOpen':[],'dateClosed':[],'priceOpen':[],'priceClosed':[],'DiffPercentage':[],'profit':[]})
df_FXEURUSD = pd.read_csv('FXEURUSD.csv', header = 0, sep= ';')
df_FXEURUSD['date'] = pd.to_datetime(df_FXEURUSD['date'], format = '%Y/%m/%d %H:%M:%S')
############              Входные данные       #################
date_start = '19-12-02 00:00:00'
date_end   = '19-12-02 23:59:00'
date_obj_s = datetime.datetime.strptime(date_start, '%y-%m-%d %H:%M:%S')
date_obj_e = datetime.datetime.strptime(date_end, '%y-%m-%d %H:%M:%S')
period_value = 20                           # каждые [period_value] минут выполняем функцию
interval_value = 30                         # интервал просматриваемого времени
actionTime_value = 40                       # время действия сделки или через сколько закрывать сделку
###########################################################################

main_function(date_obj_s,date_obj_e, period_value, interval_value, actionTime_value)

























#
