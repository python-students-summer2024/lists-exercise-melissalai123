import datetime
import os

MOODS = {
    'happy': 2,
    'relaxed': 1,
    'apathetic': 0,
    'sad': -1,
    'angry': -2
}

def get_user_mood():
    while True:
        mood = input("Enter your current mood (happy, relaxed, apathetic, sad, angry): ").strip().lower()
        if mood in MOODS:
            return mood
        else:
            print("Invalid mood. Please try again.")

def mood_to_integer(mood):
    return MOODS[mood]

def store_mood(mood):
    if not os.path.exists("data"):
        os.makedirs("data")
    
    mood_diary_path = os.path.join("data", "mood_diary.txt")
    with open(mood_diary_path, "a") as file:
        date_today = str(datetime.date.today())
        file.write(f"{date_today},{mood_to_integer(mood)}\n")

def has_already_entered_mood_today():
    mood_diary_path = os.path.join("data", "mood_diary.txt")
    if not os.path.exists(mood_diary_path):
        return False
    
    date_today = str(datetime.date.today())
    with open(mood_diary_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            date, _ = line.strip().split(',')
            if date == date_today:
                return True
    return False

def diagnose_mood():
    mood_diary_path = os.path.join("data", "mood_diary.txt")
    if not os.path.exists(mood_diary_path):
        return
    
    with open(mood_diary_path, "r") as file:
        lines = file.readlines()
        if len(lines) < 7:
            return
        
        last_7_entries = lines[-7:]
        mood_values = [int(line.strip().split(',')[1]) for line in last_7_entries]
        
        average_mood = round(sum(mood_values) / 7)
        mood_count = {
            'happy': mood_values.count(2),
            'sad': mood_values.count(-1),
            'apathetic': mood_values.count(0)
        }
        
        if mood_count['happy'] >= 5:
            diagnosis = 'manic'
        elif mood_count['sad'] >= 4:
            diagnosis = 'depressive'
        elif mood_count['apathetic'] >= 6:
            diagnosis = 'schizoid'
        else:
            diagnosis = list(MOODS.keys())[list(MOODS.values()).index(average_mood)]
        
        print(f"Your diagnosis: {diagnosis}!")

def assess_mood():
    if has_already_entered_mood_today():
        print("Sorry, you have already entered your mood today.")
        return
    
    mood = get_user_mood()
    store_mood(mood)
    diagnose_mood()