from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_interactions (
                        id INTEGER PRIMARY KEY,
                        page TEXT,
                        event_type TEXT,
                        timestamp TEXT
                      )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/log_event', methods=['POST'])
def log_event():
    data = request.json
    page = data.get('page')
    event_type = data.get('eventType')
    timestamp = datetime.now().isoformat()

    # Insert event into the database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_interactions (page, event_type, timestamp) VALUES (?, ?, ?)", (page, event_type, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'Event logged'})

@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    # Example queries to get insights
    cursor.execute("SELECT page, COUNT(*) FROM user_interactions GROUP BY page")
    page_views = cursor.fetchall()

    cursor.execute("SELECT event_type, COUNT(*) FROM user_interactions GROUP BY event_type")
    event_counts = cursor.fetchall()

    conn.close()

    return jsonify({
        'page_views': page_views,
        'event_counts': event_counts
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
