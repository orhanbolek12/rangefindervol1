import yfinance as yf

def test_formats():
    # Candidates: ABR-D, PCG-G
    # Yahoo Formats to try: "ABR-D", "ABR-PD", "ABR.PD"
    
    candidates = [
        ("ABR-D", ["ABR-D", "ABr-PD", "ABR-PD", "ABR.PD"]),
        ("PCG-G", ["PCG-G", "PCG-PG", "PCG.PG"]),
        ("JBK", ["JBK"]) # Common?
    ]
    
    for original, tries in candidates:
        print(f"\n--- Testing {original} ---")
        for t in tries:
            print(f"Trying {t}...")
            df = yf.download(t, period="1mo", progress=False)
            if not df.empty:
                print(f"SUCCESS: {t}")
                print(df.head(1))
                break
            else:
                print(f"Failed: {t}")

if __name__ == "__main__":
    test_formats()
