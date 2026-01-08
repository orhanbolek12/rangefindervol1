from logic import fetch_and_process
import time

def process_file():
    with open('tickers.txt', 'r') as f:
        content = f.read()
    
    # Split by comma or newline, cleanup
    tickers = [t.strip() for t in content.replace('\n', ',').split(',') if t.strip()]
    unique_tickers = list(set(tickers))
    print(f"Total tickers: {len(tickers)} (Unique: {len(unique_tickers)})")
    
    # Process in chunks of 50 to avoid memory/network issues and show progress
    chunk_size = 50
    all_results = []
    
    for i in range(0, len(unique_tickers), chunk_size):
        chunk = unique_tickers[i:i+chunk_size]
        print(f"Processing chunk {i}-{i+len(chunk)}...")
        
        try:
            results = fetch_and_process(chunk)
            all_results.extend(results)
            print(f"Found {len(results)} matches in this chunk.")
        except Exception as e:
            print(f"Chunk failed: {e}")
            
    print("\n\n=== FINAL RESULTS (Spread <= 1.02) ===")
    for r in all_results:
        print(r)
        
    print(f"\nTotal Matches: {len(all_results)}")

if __name__ == "__main__":
    process_file()
