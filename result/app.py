import os
from flask import Flask, render_template
import redis

app = Flask(__name__)

# Get the Redis host from the environment variable
redis_host = os.environ.get('REDIS_HOST', 'localhost')
# Connect to Redis
db = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)

@app.route('/')
def get_results():
    try:
        # Get the current vote counts. 'or 0' handles the case where the key doesn't exist yet.
        messi_votes = db.get('messi') or 0
        ronaldo_votes = db.get('ronaldo') or 0
    except redis.exceptions.ConnectionError:
        # Handle case where Redis isn't ready or is down
        messi_votes = "Error"
        ronaldo_votes = "Error"
        print("Failed to connect to Redis")

    return render_template('index.html', messi=messi_votes, ronaldo=ronaldo_votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
