def macd_strategy(df, cash, name='macd'):


    stock_held = 0  
    stock_held_column = []  
    cash_column = []        
    total_value_column = [] 


    for macd, signal, close in zip(df['macd'], df['macd_signal'], df['Close']):
        
        if macd > signal and (cash > close):
            stock_held += 1
            cash -= close

        elif (macd < signal) and (stock_held > 0):
            stock_held -= 1
            cash += close

        else:
            pass


        stock_held_column.append(stock_held)
        cash_column.append(cash)
        total_value_column.append(close * stock_held + cash)

    df['{}_stocks'.format(name)] = stock_held_column
    df['{}_cash'.format(name)] = cash_column
    df['{}_net_worth'.format(name)] = total_value_column

    return df
