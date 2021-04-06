import dateparser
from indicators import add_indicators
import pandas as pd
import os
import yfinance as yf



def _get_data(symbol, start, end, debug=False):
    cache_file_name = "cache/{sym}/{sym}_cache.csv".format(sym=symbol)
    cache_folder_name = "cache/{}".format(symbol)
    if not os.path.exists("cache"):
        os.mkdir('cache')
        print("Cache folder didn't exist. Creating it now.")
        os.mkdir(cache_folder_name)
        print("Cache folder for ${} didn't exist".format(symbol))

        df = yf.download(symbol, start=start, end=end).reset_index()
        df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in df['Date'].astype(str)]
  
        df.to_csv(cache_file_name, index=False)
        if debug == True:
            print(df.head(3))
            print(df.tail(3))
        return df

    elif (not os.path.exists(cache_folder_name)):
        os.mkdir(cache_folder_name)
        print("Cache folder for ${} didn't exist".format(symbol))
  
        df = yf.download(symbol, start=start, end=end).reset_index()
        df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in df['Date'].astype(str)]
   
        df.to_csv(cache_file_name, index=False)
        if debug == True:
            print(df.head(2))
            print(df.tail(2))
        return df

    elif not os.path.exists(cache_file_name):
       
        df = yf.download(symbol, start=start, end=end).reset_index()
        df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in df['Date'].astype(str)]
        
        df.to_csv(cache_file_name, index=False)
        print("Cache file for ${} didn't exist".format(symbol))
        if debug == True:
            print(df.head(2))
            print(df.tail(2))
        return df

    
    else:
        print("\n\nCache file for ${} exists".format(symbol))

        cached_df = pd.read_csv(cache_file_name, header=0, index_col=False)

        cached_df['Date'] = [dateparser.parse(i, date_formats=['%m/%d/%y']) for i in cached_df['Date'].astype(str)]
        start = dateparser.parse(start, date_formats=['%m/%d/%y'])
        end = dateparser.parse(end, date_formats=['%m/%d/%y'])

        first_date_in_cache = cached_df['Date'].iloc[0]
        first_date_in_cache = dateparser.parse(str(first_date_in_cache), date_formats=['%m/%d/%y'])
        last_date_in_cache = cached_df['Date'].iloc[len(cached_df)-1]
        last_date_in_cache = dateparser.parse(str(last_date_in_cache), date_formats=['%m/%d/%y'])

        if debug == True:
            print("Start : ", start, " // first_date_in_cache : ", first_date_in_cache)
            print("End : ", end, " // last_date_in_cache : ", last_date_in_cache)


        if (first_date_in_cache <= start) and (last_date_in_cache >= end):
         
            cached_df = cached_df[(cached_df['Date'] >= start)]
            cached_df = cached_df[(cached_df['Date'] <= end)]
            print("${} cache had all necessary data, returning cached data.".format(symbol))
            if debug == True:
                print(cached_df.head(3))
                print(cached_df.tail(3))
            return cached_df

        elif first_date_in_cache <= start and last_date_in_cache <= end:

            download_df = yf.download(symbol, last_date_in_cache, end).reset_index()

            cached_df = cached_df.append(download_df, ignore_index=True, sort=False)

            cached_df = cached_df.sort_values(by='Date')
            cached_df = cached_df.drop_duplicates()
 
            os.unlink(cache_file_name)

            cached_df.to_csv(cache_file_name, index=False)
            print("${} cache had earlier data but not through requested end, cache has been updated.".format(symbol))
            if debug == True:
                print(cached_df.head(3))
                print(cached_df.tail(3))
            return cached_df

        elif first_date_in_cache >= start and last_date_in_cache >= end:

            download_df = yf.download(symbol, start, first_date_in_cache).reset_index()

            cached_df = cached_df.append(download_df, ignore_index=True)
            cached_df = cached_df.sort_values(by='Date')
            cached_df = cached_df.drop_duplicates()
            os.unlink(cache_file_name)
            cached_df.to_csv(cache_file_name, index=False)
            print("${} cache had later data but not as early as requested, cache has been updated.".format(symbol))
            if debug == True:
                print(cached_df.head(3))
                print(cached_df.tail(3))
            return cached_df

        else:
            if debug == True:
                print("Please help me, I'm on fire.")
            return None


def get_dataframe(symbol, start, end, debug, cache=True):

    if cache == True:
        df = _get_data(symbol, start, end, debug)
        sp_df = _get_data('SPY', start, end, debug)
    elif cache == False:
        df = yf.download(symbol, start=start, end=end).reset_index()
        sp_df = yf.download('SPY', start=start, end=end).reset_index()
    df = add_indicators(df)

    df['sp_500_close'] = sp_df['Close']
    print('\n\n')
    return df
