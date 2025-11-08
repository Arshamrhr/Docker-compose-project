import os
from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)

# Get the Redis host from the environment variable we set in docker-compose
redis_host = os.environ.get('REDIS_HOST', 'localhost')
# Connect to Redis
# decode_responses=True is important to get strings, not bytes
db = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the vote from the form button
        vote = request.form['vote']
        
        # Increment the counter in Redis for the chosen player
        if vote == 'messi':
            db.incr('messi')
        elif vote == 'ronaldo':
            db.incr('ronaldo')
            
        # Redirect back to the index page (prevents re-voting on refresh)
        return redirect(url_for('index'))

    # On a GET request, just show the page
    return render_template('index.html')

if __name__ == '__main__':
    # Run the app on port 80, accessible from anywhere (0.0.0.0)
    app.run(host='0.0.0.0', port=80, debug=True)
