import sqlite3
import urllib.request
import json
import sys

def init_db():
    conn = sqlite3.connect('twd_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episode_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_num INTEGER NOT NULL,
            episode_title TEXT NOT NULL,
            choice_description TEXT NOT NULL,
            percentage TEXT NOT NULL
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM episode_stats')
    if cursor.fetchone()[0] == 0:
        sample_stats = [
            (1, 'A New Day', 'Saved Duck instead of Shawn', '49%'),
            (1, 'A New Day', 'Saved Carley instead of Doug', '76%'),
            (2, 'Starved for Help', 'Helped Kenny kill Larry', '75%'),
            (2, 'Starved for Help', 'Stole food from the car', '54%'),
            (3, 'Long Road Ahead', 'Left Lilly behind', '58%'),
            (3, 'Long Road Ahead', 'Put Duck out of his misery', '82%'),
            (4, 'Around Every Corner', 'Kept the bite a secret', '41%'),
            (5, 'No Time Left', 'Shot Lee at the end', '74%')
        ]
        cursor.executemany('''
            INSERT INTO episode_stats (episode_num, episode_title, choice_description, percentage)
            VALUES (?, ?, ?, ?)
        ''', sample_stats)
        conn.commit()
    conn.close()

def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get('response', '')
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def handle_episodes_command():
    conn = sqlite3.connect('twd_stats.db')
    cursor = conn.cursor()
    
    ep_input = input("Enter Episode Number (1-5): ").strip()
    if not ep_input.isdigit():
        print("Invalid input. Enter an integer between 1 and 5.")
        conn.close()
        return
        
    ep_num = int(ep_input)
    cursor.execute("SELECT episode_title, choice_description, percentage FROM episode_stats WHERE episode_num = ?", (ep_num,))
    rows = cursor.fetchall()
    
    if rows:
        print(f"\n--- EPISODE {ep_num}: {rows[0][0]} - PLAYER STATS ---")
        for row in rows:
            print(f"• {row[1]}: **{row[2]}** of players")
    else:
        print(f"\nNo stats found for Episode {ep_num}.")
    
    conn.close()
    print("-" * 50 + "\n")

def main():
    init_db()
    print("==========================================")
    print(" THE WALKING DEAD SEASON 1 ASSISTANT      ")
    print("==========================================")
    print("Chat with Lee or type '/episodes' to view global Telltale choice percentages.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        if user_input.lower() == '/exit':
            break
        if user_input.lower() == '/episodes':
            handle_episodes_command()
            continue

        # Hardened system prompt: focused on game choice strategy and group survival, 
        # explicitly banning medical fanfic and fake physics.
        system_prompt = (
            "You are Lee Everett from The Walking Dead Season 1, acting as a strategic advisor for a choice-driven narrative game. "
            "Give practical, grounded advice on handling tough moral dilemmas, managing group trust and relationships (like Kenny and Larry), "
            "and weighing the narrative consequences of player choices. "
            "Strictly ban fake medical treatments, zombie physics, or invented game mechanics. "
            "Keep answers concise, realistic, and focused on survival choices a player actually faces."
        )
        full_prompt = f"{system_prompt}\n\nUser Situation: {user_input}\nLee's Response:"
        
        print("\nThinking...")
        response = query_ollama(full_prompt)
        print(f"\nLee: {response}\n")

if __name__ == "__main__":
    main()

