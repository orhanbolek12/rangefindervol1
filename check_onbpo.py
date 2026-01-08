import yfinance as yf
import pandas as pd

def check_onbpo():
    ticker_name = "ONBPO" 
    # Try finding the right ticker format if ONBPO fails (ONB-PO? ONB-O?)
    # Using previous finding logic: ONBPO -> ONB-PO maybe? Or just ONBPO if it's preferred.
    # Actually ONBPO is often ONB-PO on Yahoo.
    
    candidates = ["ONBPO", "ONB-PO", "ONB.PO", "ONB-O"]
    df = pd.DataFrame()
    
    for t in candidates:
        print(f"Checking {t}...")
        d = yf.Ticker(t).history(period="3mo", auto_adjust=True) # 3mo is approx 90 days
        if not d.empty:
            print(f"Found data for {t}")
            df = d
            break
            
    if df.empty:
        print("Could not fetch ONBPO data.")
        return

    # Filter 1: Average Daily Spread >= 0.10
    daily_spreads = df['High'] - df['Low']
    avg_daily_spread = daily_spreads.mean()
    
    # Filter 2: Total Range <= 1.00 (Max High - Min Low)
    # User said "1 puandan eşit ve düşük" -> <= 1.0
    total_high = df['High'].max()
    total_low = df['Low'].min()
    total_range = total_high - total_low
    
    print(f"\n--- Analysis for {ticker_name} (Last ~90 Days) ---")
    print(f"Data Points: {len(df)}")
    print(f"Avg Daily Spread: ${avg_daily_spread:.4f} (Target >= 0.10)")
    print(f"Total Range: ${total_range:.4f} (Target <= 1.00)")
    print(f"Min Low: {total_low}, Max High: {total_high}")
    
    pass_volatility = avg_daily_spread >= 0.10
    pass_range = total_range <= 1.02 # User said 1 point, let's see if 1.02 is better or strict 1.0
    
    print(f"\nPasses Avg Volatility? {pass_volatility}")
    print(f"Passes Range (<= 1.02)? {pass_range}")
    print(f"Passes Range (<= 1.00)? {total_range <= 1.00}")

if __name__ == "__main__":
    check_onbpo()
