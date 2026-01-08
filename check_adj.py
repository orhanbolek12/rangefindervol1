from tvDatafeed import TvDatafeed, Interval
import yfinance as yf
import pandas as pd

def check_adjustment():
    tv = TvDatafeed()
    
    # Fetch ABR from TradingView
    print("Fetching TV Data for ABR...")
    tv_df = tv.get_hist(symbol='ABR', exchange='NYSE', interval=Interval.in_daily, n_bars=150)
    
    # Fetch ABR from YFinance (Auto adjusted)
    print("Fetching YF Data for ABR...")
    yf_df = yf.download("ABR", period="6mo", auto_adjust=True) # auto_adjust=True gives Adj Close
    
    # Sync Dates
    # TV index is datetime, YF is datetime
    # Let's look at the last few rows overlap
    
    if tv_df is not None and not yf_df.empty:
        # Get a common date
        last_date = tv_df.index[-1]
        # YF might have time info or just date
        
        # Simple comparison of the last 5 closes
        print("\n--- Comparison ---")
        print("TradingView Tail (Close):")
        print(tv_df['close'].tail())
        
        print("\nYFinance Tail (Close - Adjusted):")
        print(yf_df['Close'].tail())
        
        # Check specific date deviation
        # Pick a date 3 months ago (likely before last div)
        try:
             # Find a date in both
             common_idx = tv_df.index.intersection(yf_df.index)
             if not common_idx.empty:
                 date = common_idx[0] # earliest common
                 tv_price = tv_df.loc[date]['close']
                 yf_price = yf_df.loc[date]['Close']
                 
                 # YF has 'Close' as Adj Close when auto_adjust=True
                 print(f"\nDate: {date}")
                 print(f"TV Close: {tv_price}")
                 print(f"YF Adj Close: {yf_price}")
                 
                 if abs(tv_price - yf_price) < 0.1:
                     print("CONCLUSION: TV Data is LIKELY ADJUSTED.")
                 else:
                     print("CONCLUSION: TV Data is LIKELY RAW (Not Adjusted).")
             else:
                 print("No common dates found?")
        except Exception as e:
            print(f"Error converting indices: {e}")

if __name__ == "__main__":
    check_adjustment()
