import requests
import time

def test_api():
    base_url = "http://127.0.0.1:5000"
    
    # 1. Start Job
    print("Sending request...")
    # Use a small subset including one that should pass and one that should fail filter
    # ABR-D (ABR/PD) - might pass or fail depending on volatility.
    # JBK - likely common or pref.
    tickers = "ABR-D, JBK" 
    
    try:
        resp = requests.post(f"{base_url}/find", data={'tickers': tickers})
        if resp.status_code != 200:
            print("Error starting job:", resp.text)
            return
            
        job_id = resp.json()['job_id']
        print(f"Job started: {job_id}")
        
        # 2. Poll Status
        while True:
            status_resp = requests.get(f"{base_url}/status/{job_id}")
            status_data = status_resp.json()
            
            print(f"Status: {status_data['status']}, Progress: {status_data.get('progress')}/{status_data.get('total')}")
            
            if status_data['status'] == 'completed':
                print("\nJob Completed!")
                print("Results:")
                print(status_data['results'])
                break
            
            time.sleep(2)

    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    test_api()
