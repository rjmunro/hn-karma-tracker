import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from pathlib import Path

def get_karma(user_id):
    """Fetch karma points for a given user from Hacker News."""
    url = f"https://news.ycombinator.com/user?id={user_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find karma value - updated selector based on actual HTML structure
    karma_row = soup.find('td', string='karma:')
    if karma_row:
        karma_value = karma_row.find_next_sibling('td').text
        try:
            return int(karma_value)
        except ValueError:
            print(f"Failed to convert karma value '{karma_value}' to integer")
            return None
    else:
        print("Could not find karma row in HTML")
        return None

def update_karma_history(karma_value):
    """Update the karma history JSON file with new karma value."""
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)

    history_file = data_dir / 'karma_history.json'

    # Load existing data or create new
    if history_file.exists():
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = []

    # Add new entry
    today = datetime.now().strftime('%Y-%m-%d')

    # Check if we already have an entry for today
    today_entry = next((item for item in history if item['date'] == today), None)
    if today_entry:
        today_entry['karma'] = karma_value
    else:
        history.append({
            'date': today,
            'karma': karma_value
        })

    # Save updated data
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def main():
    user_id = os.environ.get('HN_USER_ID', 'nkko')  # Default to 'nkko' if env var not set
    print(f"Fetching karma for user: {user_id}")

    karma = get_karma(user_id)
    if karma is not None:
        print(f"Successfully fetched karma: {karma}")
        update_karma_history(karma)
        print("Updated karma history")
    else:
        raise ValueError("Failed to fetch karma points")

if __name__ == "__main__":
    main()