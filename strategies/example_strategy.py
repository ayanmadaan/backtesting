def example_strategy(df, cash, name='example'):


    stock_held = 0 
    stock_held_column = []  
    cash_column = []        
    total_value_column = [] 

    for close, diff in zip(df['Close'], df['day_difference']):
  
        if diff > 2:
            stock_held += 1
            cash -= close

        elif (diff < -2) and (stock_held > 0):
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
