import json
from flask import Flask,render_template,request,jsonify
import pandas as pd
import random
from datetime import datetime
import glob
import plotly.graph_objects as go
from candlestick import candlestick

app =Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/display_data', methods=['POST'])
def display_dataset():
    dataset = request.form['dataset']
    table_data=""
    if dataset == "2000-2004":
        data = pd.read_csv('Dataset/apple_1.csv')
        data= data.drop(['AdjClose'], axis=1)
        table_data = data.to_json(orient='records')
        return jsonify(table_data)
    elif dataset == "2005-2009":
        data = pd.read_csv('Dataset/apple_2.csv')
        data= data.drop(['AdjClose'], axis=1)

        table_data = data.to_json(orient='records')
        return jsonify(table_data)
    elif dataset == "2010-2014":
        data = pd.read_csv('Dataset/apple_3.csv')
        data= data.drop(['AdjClose'], axis=1)

        table_data = data.to_json(orient='records')
        return jsonify(table_data)
    elif dataset == "2015-2019":
        data = pd.read_csv('Dataset/apple_4.csv')
        data= data.drop(['AdjClose'], axis=1)

        table_data = data.to_json(orient='records')
        return jsonify(table_data)
    elif dataset == "2019-2022":
        data = pd.read_csv('Dataset/apple_5.csv')
        data= data.drop(['AdjClose'], axis=1)
        table_data = data.to_json(orient='records')
        return jsonify(table_data)
    

@app.route('/merge_dataset')
def merge_dataset(): 
    csv_directory = './Dataset/'
    csv_pattern = '*.csv'
    csv_files = glob.glob(csv_directory + csv_pattern)
    dataframes = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dataframes.append(df)

    merged_data = pd.concat(dataframes, ignore_index=True)
    merged_data = merged_data.drop("AdjClose", axis=1)
    merged_csv_path = './Dataset/MergedDataset/merged_dataset.csv'
    merged_data.to_csv(merged_csv_path, index=False)
   
    return render_template('MergeDataset.html' , dataset=merged_data)

   
@app.route('/analyze_dataset' , methods=["POST"])
def analyze_dataset(): 
    apple = pd.read_csv('Dataset/MergedDataset/merged_dataset.csv')
    length = len(apple)
    
    date_missing = find_missing('Date',apple)
    high_missing = find_missing('High',apple)
    low_missing = find_missing('Low',apple)
    open_missing = find_missing('Open',apple)
    close_missing = find_missing('Close',apple)
    volume_missing = find_missing('Volume',apple)
#   [1,2,3,4,5]  --- { 0: 1 , 1:2 , 2:3} 
    date_missing_percent = find_missing_percent(date_missing,length)
    high_missing_percent = find_missing_percent(high_missing,length)
    open_missing_percent = find_missing_percent(open_missing,length)
    low_missing_percent = find_missing_percent(low_missing,length)
    close_missing_percent = find_missing_percent(close_missing,length)
    volume_missing_percent = find_missing_percent(volume_missing,length)

    analyzed_data= {
        "Date" : date_missing_percent,
        "Open" : open_missing_percent,
        "High" : high_missing_percent,
        "Low"  : low_missing_percent,
        "Close": close_missing_percent,
        "Volume": volume_missing_percent
    }
    
    return json.dumps(analyzed_data)

def find_missing(column,apple):
    return apple[column].isna().sum()

def find_missing_percent(count,length):
    return (count/length)*100

Cleanapple = ""
 
@app.route('/clean_dataset' , methods=["POST"])
def clean_dataset():
    global Cleanapple
    Cleanapple = pd.read_csv('Dataset/MergedDataset/merged_dataset.csv')
    
    while(True):
        if find_missing("Date",Cleanapple) > 0:
            fixing_date(Cleanapple)
        else:
            break
    clean_low(Cleanapple)
    clean_high(Cleanapple)
    clean_open(Cleanapple)
    clean_close(Cleanapple)
    clean_volume(Cleanapple)
    remove_outliers(Cleanapple)

    return render_template( "CleanDataset.html" , dataset=Cleanapple) 

def remove_outliers(apple):
    new_apple = apple
    new_apple = new_apple.loc[~((new_apple['Low'] == new_apple['High']))]
    new_apple = new_apple.reset_index()
    new_apple = new_apple.drop(['index'], axis=1)
    return new_apple

def fixing_miss(index, no_nb, column,apple):
    iter_x = no_nb
    iter_y = no_nb
    null_lower_sum = 0
    null_upper_sum = 0
    index=index-1
    # print(index)
    for j in range(iter_x):
        val = (index-j), apple[column][index-j]
        if pd.isna(val[1]):
            iter_x = iter_x + 1
            continue
        else:
            null_lower_sum = null_lower_sum + val[1]
    #       print(val[1])  
        index=index+2
#         print(index)
    for k in range(iter_y):
        val = (index+k), apple[column][index+k]
        if pd.isna(val[1]):
            iter_y = iter_y + 1
            continue
        else:
            null_upper_sum = null_upper_sum + val[1]
#             print(val[1])

    print(null_lower_sum)
    print(null_upper_sum)
    total = null_lower_sum+null_upper_sum
    total = total/(no_nb*2)
    print(total)
    return total

def fixing_date(apple):
    iter_x = 1
    iter_y = 1
    if find_missing("Date",apple) > 0:
        for index in range(len(apple)):
#             print(apple['Date'][index])
            if pd.isna(apple['Date'][index]):
#                 print(apple['Date'][index])
                org_index = index
                index=index-1
                # print(index)
                for j in range(iter_x):
                    val = (index-j), apple["Date"][index-j]
#                     print(val)
                    if pd.isna(val[1]):
                        iter_x = iter_x + 1
                        continue
                    else:
                        lower_date = val[1]
#                         print(val[1])  

                    index=index+2
#                     print(index)
                for k in range(iter_y):
                    val = (index+k), apple["Date"][index+k]
                    # print(val)
                    if pd.isna(val[1]):
                        iter_y = iter_y + 1
                        continue
                    else:
                        upper_date = val[1]
#                       print(val[1])
          
            else:
#                 print(apple['Date'][index])
                  pass

    
    lower_day_comp = lower_date.split('/')   
    lower_day = lower_day_comp[1]
    lower_day = int(lower_day)

    upper_day_comp = upper_date.split('/')    
    upper_day = upper_day_comp[1]
    upper_day = int(upper_day)


    if lower_day == 30:
        if upper_day == 1:
            day = 31
            day=str(day)
            lower_day_comp[1] = day
            day = '/'.join(lower_day_comp)
        else:
            day = 1
            day=str(day)
            upper_day_comp[1] = day
            day = '/'.join(upper_day_comp)
    elif lower_day == 31:
        day = 1
        day=str(day)
        lower_day_comp[1] = day
        day = '/'.join(upper_day_comp)
    else:
    #     lower_date = str(lower_date)
    #     upper_date = str(upper_date)

        # convert string to date object
        d1 = datetime.strptime(lower_date, "%m/%d/%Y")
        d2 = datetime.strptime(upper_date, "%m/%d/%Y")

        # difference between dates in timedelta
        delta = d2 - d1
        day=delta.days-1
        print(day)
        day= random.randint(1, day)
        day=day+lower_day
        day=str(day)
        lower_day_comp[1] = day
        day = '/'.join(lower_day_comp)
    apple['Date'][org_index]=day

def clean_low(apple):
    if find_missing("Low",apple) > 0:
        for i in range(len(apple)):
    #         print(i, apple['Low'][i])
            if pd.isna(apple['Low'][i]):
                print("Missing value!")
                val=fixing_miss(i,1,'Low',apple)
    #             print(val)
                if val <= apple['Open'][i] and val <= apple['Close'][i] and val < apple['High'][i]:
                    apple['Low'][i] = val
    #                 print(val)
                else:
                    if apple['Open'][i] < apple['Close'][i]:
                        apple['Low'][i] = apple['Open'][i]
                    else:
                        apple['Low'][i] = apple['Close'][i]
            else:
                pass
            
def clean_high(apple):
    if find_missing("High",apple) > 0:
        for i in range(len(apple)):
    #         print(i, apple['High'][i])
            if pd.isna(apple['High'][i]):
                print("Missing value!")
                val=fixing_miss(i,1,'High',apple)
    #             print(val)
                if val >= apple['Open'][i] and val >= apple['Close'][i] and val > apple['Low'][i]:
                    apple['High'][i] = val
    #                 print(val)
                else:
                    if apple['Open'][i] > apple['Close'][i]:
                        apple['High'][i] = apple['Open'][i]
                    else:
                        apple['High'][i] = apple['Close'][i]
            else:
                pass
     
def clean_open(apple):    
    if find_missing("Open",apple) > 0:
        for i in range(len(apple)):
    #         print(i, apple['Open'][i])
            if pd.isna(apple['Open'][i]):
                print("Missing value!")
                val=fixing_miss(i,1,'Open',apple)
    #             print(val)
                if val >= apple['Low'][i] and val <= apple['High'][i]:
                    apple['Open'][i] = val
    #                 print(val)
                else:
                    if val < apple['Low'][i]:
                        apple['Open'][i] = apple['Low'][i]
                    else:
                        apple['Open'][i] = apple['High'][i]
            else:
                pass

def clean_close(apple):
    if find_missing("Close",apple) > 0:
        for i in range(len(apple)):
    #         print(i, apple['Close'][i])
            if pd.isna(apple['Close'][i]):
                val=fixing_miss(i,1,'Close',apple)
    #             print(val)
                if val >= apple['Low'][i] and val <= apple['High'][i]:
                    apple['Close'][i] = val
    #                 print(val)
                else:
                    if val < apple['Low'][i]:
                        apple['Close'][i] = apple['Low'][i]
                    else:
                        apple['Close'][i] = apple['High'][i]
            else:
                pass
            
def clean_volume(apple):
    if find_missing("Volume",apple) > 0:
        for i in range(len(apple)):
            if pd.isna(apple['Volume'][i]):
                val=fixing_miss(i,1,'Volume',apple)
                apple['Volume'][i] = val
            else:
                pass


@app.route('/insight_data', methods=['POST'])
def insight_data(): 
    data = request.get_json()

    date_object = datetime.strptime(data["from_date"], '%Y-%m-%d')
    from_date = date_object.strftime('%m/%d/%Y')

    date_object = datetime.strptime(data["to_date"], '%Y-%m-%d')
    to_date = date_object.strftime('%m/%d/%Y')

    if(data["indicators"]== "date_wise"):
        response_data = plot_range_date(from_date,to_date)
        return jsonify({'graph_html': response_data})
    
    elif(data["indicators"]== "SMA-EMA"):
        response_data = moving_average(from_date,to_date,int(data["sma_days"]),int(data["ema_days"]))
        return jsonify({'graph_html': response_data})
    
    elif(data["indicators"]== "RSI"):
        response_data = relative_strength_index(from_date,to_date)
        return jsonify({'graph_html': response_data})
    
    elif(data["indicators"]== "InHammer"):
        symbol="diamond-open"
        response_data = candle_stick(from_date,to_date,"InvertedHammer",symbol,"Inverted Hammer")
        return jsonify({'graph_html': response_data})
    
    elif(data["indicators"]== "DojiStar"):
        symbol="x"
        response_data = candle_stick(from_date,to_date,"DojiStar",symbol,"Doji Star")
        return jsonify({'graph_html': response_data})
    
    elif(data["indicators"]== "HangingMan"):
        symbol="triangle-down"
        response_data = candle_stick(from_date,to_date,"HangingMan",symbol,"Hanging Man")
        return jsonify({'graph_html': response_data})


def moving_average(start_date,end_date,n,ew):

    # Simple Moving Average 
    def SMA(data, ndays): 
        SMA = pd.Series(data['Close'].rolling(ndays).mean(), name = 'SMA') 
        data = data.join(SMA) 
        return data

    # Exponentially-weighted Moving Average 
    def EWMA(data, ndays): 
        EMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                     name = 'EWMA_' + str(ndays)) 
        data = data.join(EMA) 
        return data

    # Retrieve the Goolge stock data from Yahoo finance
    data = range_date(start_date,end_date)
    close = data['Close']
    str_n = str(n)
    str_ew = str(ew)
    
    # Compute the 50-day SMA
    sma_tag = 'SMA'
    SMA = SMA(data,n)
    SMA = SMA.dropna()
    SMA = SMA[sma_tag]

    # Compute the 200-day EWMA
    ewma_tag = 'EWMA_'+str_ew
    EWMA = EWMA(data,ew)
    EWMA = EWMA.dropna()
    EWMA = EWMA[ewma_tag]

    # Create the figure
    fig = go.Figure()

    # Plot close price and moving averages
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=SMA, name=str_n + '-day SMA', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=data['Date'], y=EWMA, name=str_ew + '-day EWMA', line=dict(color='red')))

    # Set the title and axis labels
    fig.update_layout(
        title='Moving Average',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    fig.update_layout(autosize=True, height=300, margin=dict(l=40, r=40, b=40, t=40))
    
    graph_html = fig.to_html(full_html=False)
    return graph_html


def range_date(start_date,end_date):
    new_apple = Cleanapple
    new_apple.Date=pd.to_datetime(new_apple.Date)
    new_apple = new_apple.loc[new_apple['Date'].between(start_date,end_date, inclusive='both')]
    new_apple = new_apple.reset_index()
    new_apple = new_apple.drop(['index'], axis=1)
    return new_apple


def plot_range_date(start_date,end_date):

    date = range_date(start_date,end_date)      
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date['Date'], y=date['Close'], name='Close', line=dict(color='firebrick')))
    fig.add_trace(go.Scatter(x=date['Date'], y=date['Open'], name='Open', line=dict(color='blue')))
    
    fig.update_layout(title="The Stock Price of Apple",
                      xaxis_title="Date",
                      yaxis_title="Price",
    )
    fig.update_layout(autosize=True, height=350, margin=dict(l=40, r=40, b=40, t=40))
    
    graph_html = fig.to_html(full_html=False)
    return graph_html


def relative_strength_index(start_date, end_date):
    
    def rsi(close, periods=14):
        close_delta = close.diff()
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        rsi = ma_up / ma_down
        rsi = 100 - (100 / (1 + rsi))
        return rsi

    data = range_date(start_date, end_date)

    data['RSI'] = rsi(data['Close'])

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['Date'],
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name='Candlestick'))

    fig.add_trace(go.Scatter(x=data['Date'],
                             y=data['RSI'],
                             name='RSI',
                             line=dict(color='magenta')))

    fig.update_layout(title='Apple Price Chart and RSI',
                      xaxis_title='Date',
                      yaxis_title='Price / RSI')
    fig.update_layout(autosize=True, height=400, margin=dict(l=40, r=40, b=40, t=40))


    graph_html = fig.to_html(full_html=False)
    return graph_html


def candle_stick(from_date,to_date,pattern,pattern_symbol,pattern_name):
    
    df = Cleanapple
    df['Date'] = pd.to_datetime(df['Date'])    
    start_date = from_date
    end_date = to_date
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if(pattern == "InvertedHammer"):
        stock = candlestick.inverted_hammer(filtered_df, ohlc=['Open', 'High', 'Low', 'Close'], target='result')
    
    elif(pattern == "HangingMan"):
        stock = candlestick.hanging_man(filtered_df, ohlc=['Open', 'High', 'Low', 'Close'], target='result')
    
    elif(pattern == "DojiStar"):
        stock = candlestick.doji_star(filtered_df, ohlc=['Open', 'High', 'Low', 'Close'], target='result')
    
    stock.loc[stock['result'] != False, 'nova'] = stock['Close']
    
    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=filtered_df['Date'],
        open=stock['Open'],
        high=stock['High'],
        low=stock['Low'],
        close=stock['Close']
    )])
    
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=stock["nova"],
        name=pattern_name,
        mode="markers",
        marker_color='rgba(0, 0, 255, .9)',
        marker=dict(symbol=pattern_symbol)
    ))
    fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
    )
    fig.update_layout(autosize=True, height=400, margin=dict(l=40, r=40, b=40, t=40))

    
    
    graph_html = fig.to_html(full_html=False)
    return graph_html

if __name__=="__main__":
    app.run(debug=True)