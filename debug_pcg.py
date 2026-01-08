from tvDatafeed import TvDatafeed, Interval
import yfinance as yf
import pandas as pd

def debug_pcg():
    tv = TvDatafeed()
    
    # 1. Check what logic.py does: PCG-G -> PCG/PG
    # The user's list had PCG-G. 
    # Logic: if '-' in ticker -> split -> base + '/P' + suffix.
    # PCG-G -> PCG/PG.
    
    tv_symbol = 'PCG/PG'
    print(f"Fetching {tv_symbol} from TV...")
    df = tv.get_hist(symbol=tv_symbol, interval=Interval.in_daily, n_bars=150)
    
    if df is not None:
        print("TV Data Head:")
        print(df.head())
        print("TV Data Tail:")
        print(df.tail())
        print(f"Min: {df['low'].min()}, Max: {df['high'].max()}")
    else:
        print("TV returned None")

    # 2. Compare with YFinance
    # PCG-G in Yahoo is usually PCG-PG or PCG-pG? 
    # Yahoo preferreds often: "PCG-PG" or "PCG-P-G" or "PCG-G" depending on the day.
    # Let's try likely candidates.
    yf_tickers = ["PCG-PG", "PCG-G", "PCG.PG"]
    
    for t in yf_tickers:
        print(f"\nFetching {t} from YF...")
        yf_data = yf.download(t, period="6mo", auto_adjust=True)
        if not yf_data.empty:
            print(f"YF {t} Tail:")
            print(yf_data.tail())
            print(f"YF Min: {yf_data['Low'].min()}, YF Max: {yf_data['High'].max()}")
        else:
            print(f"YF {t} returned empty")

if __name__ == "__main__":
    debug_pcg()
