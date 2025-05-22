import sched, time, sqlite3
from datetime import datetime

s = sched.scheduler(time.time, time.sleep)

def check_reminders():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT title, due_time FROM tasks")
    tasks = c.fetchall()
    for title, due_time in tasks:
        try:
            due = datetime.strptime(due_time, "%Y-%m-%dT%H:%M")
            now = datetime.now()
            delta = (due - now).total_seconds()
            if 0 < delta < 300:
                print(f"🔔 Rappel : '{title}' est prévu à {due_time}")
        except Exception as e:
            print(f"Erreur de rappel : {e}")
    conn.close()
    s.enter(60, 1, check_reminders)

def start_scheduler():
    s.enter(1, 1, check_reminders)
    s.run()
