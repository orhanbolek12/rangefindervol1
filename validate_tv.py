from tvDatafeed import TvDatafeed, Interval
import pandas as pd

def validate():
    tv = TvDatafeed()
    
    # Test 1: Fetch Common Stock (ABR)
    print("Fetching ABR (Common)...")
    try:
        abr = tv.get_hist(symbol='ABR', exchange='NYSE', interval=Interval.in_daily, n_bars=150)
        if abr is not None:
            print("ABR Data Head:")
            print(abr.head())
            print("ABR Data Tail:")
            print(abr.tail())
            print("Columns:", abr.columns)
        else:
            print("ABR fetch returned None")
    except Exception as e:
        print(f"Error fetching ABR: {e}")

    # Test 2: Fetch Preferred Stock (ABR-D converted to ABR/PD)
    symbol_pref = 'ABR/PD'
    print(f"\nFetching {symbol_pref}...")
    try:
        # Note: Exchange is likely NYSE for ABR preferreds too.
        # TvDatafeed sometimes needs just the symbol if exchange is 'NYSE', or might be tricky with special chars.
        abr_pref = tv.get_hist(symbol=symbol_pref, exchange='NYSE', interval=Interval.in_daily, n_bars=150)
        if abr_pref is None:
            # Try without exchange specified (TvDatafeed searches)
             print(f"Direct fetch failed, trying search for {symbol_pref}...")
             abr_pref = tv.get_hist(symbol=symbol_pref, exchange='NYSE', interval=Interval.in_daily, n_bars=150)
        
        if abr_pref is not None:
            print(f"{symbol_pref} Data Head:")
            print(abr_pref.head())
            print(f"{symbol_pref} Data Tail:")
            print(abr_pref.tail())
        else:
            print(f"{symbol_pref} fetch returned None")

    except Exception as e:
        print(f"Error fetching {symbol_pref}: {e}")

if __name__ == "__main__":
    validate()
