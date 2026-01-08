from flask import Flask, render_template, request, jsonify
from logic import fetch_and_process
import threading
import uuid
import time

app = Flask(__name__)

# In-memory storage
jobs = {}
prefs_cache = {
    'status': 'idle', # idle, processing, completed
    'last_updated': None,
    'results': [],
    'progress': 0,
    'total': 0
}

def load_and_analyze_prefs():
    """Background task to analyze the big list from tickers.txt"""
    global prefs_cache
    prefs_cache['status'] = 'processing'
    
    try:
        with open('tickers.txt', 'r') as f:
            content = f.read()
        
        tickers = [t.strip() for t in content.replace('\n', ',').split(',') if t.strip()]
        unique_tickers = list(set(tickers))
        prefs_cache['total'] = len(unique_tickers)
        
        def update_progress(current, total):
            prefs_cache['progress'] = current

        # Run logic
        results = fetch_and_process(unique_tickers, progress_callback=update_progress)
        
        prefs_cache['results'] = results
        prefs_cache['status'] = 'completed'
        prefs_cache['last_updated'] = time.ctime()
        print(f"Prefs Analysis Completed. Found {len(results)} matches.")
        
    except Exception as e:
        print(f"Error in background prefs analysis: {e}")
        prefs_cache['status'] = 'error'

# Start background thread for prefs on startup
threading.Thread(target=load_and_analyze_prefs, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prefs', methods=['GET'])
def get_prefs():
    return jsonify(prefs_cache)

@app.route('/refresh_prefs', methods=['POST'])
def refresh_prefs():
    if prefs_cache['status'] == 'processing':
        return jsonify({'status': 'processing', 'message': 'Already strictly running'})
    
    threading.Thread(target=load_and_analyze_prefs, daemon=True).start()
    return jsonify({'status': 'started'})

@app.route('/find', methods=['POST'])
def find_spreads():
    raw_text = request.form.get('tickers', '')
    if not raw_text:
        return jsonify({'error': 'No tickers provided'}), 400
    
    # Split by comma or newline
    tickers = [t.strip() for t in raw_text.replace('\n', ',').split(',') if t.strip()]
    
    job_id = str(uuid.uuid4())
    jobs[job_id] = {'status': 'processing', 'progress': 0, 'total': len(tickers), 'results': []}
    
    # Start processing in background thread
    thread = threading.Thread(target=process_job, args=(job_id, tickers))
    thread.start()
    
    return jsonify({'job_id': job_id})

def process_job(job_id, tickers):
    def update_progress(current, total):
        jobs[job_id]['progress'] = current
        
    results = fetch_and_process(tickers, progress_callback=update_progress)
    jobs[job_id]['results'] = results
    jobs[job_id]['status'] = 'completed'

@app.route('/status/<job_id>')
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job)

@app.route('/result_item/<job_id>')
def get_results(job_id):
    # This might be redundant if status returns results, but kept for clarity if needed
    job = jobs.get(job_id)
    if job and job['status'] == 'completed':
        return jsonify(job['results'])
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
