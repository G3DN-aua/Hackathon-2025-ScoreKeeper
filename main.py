import tkinter as tk
from tkinter import simpledialog, messagebox
import os

MATCH_FILE = "matches.txt"

matches = {}
current_match = None

def save_matches():
    with open(MATCH_FILE, "w") as f:
        for match, data in matches.items():
            line = f"{match},{data['team1_name']},{data['team1_score']},{data['team2_name']},{data['team2_score']},{data['locked']}\n"
            f.write(line)

def load_matches():
    if not os.path.exists(MATCH_FILE):
        return

    with open(MATCH_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 6:
                match, team1_name, team1_score, team2_name, team2_score, locked = parts
                matches[match] = {
                    "team1_name": team1_name,
                    "team1_score": int(team1_score),
                    "team2_name": team2_name,
                    "team2_score": int(team2_score),
                    "locked": locked
                }
                match_listbox.insert(tk.END, match)

def start_scoring(match_name):
    global current_match
    current_match = match_name

    if matches[match_name]["locked"] == "locked":
        response = messagebox.askyesno("Locked Match", f"{match_name} is locked. Do you want to unlock and edit?")
        if not response:
            return
        else:
            matches[match_name]["locked"] = "unlocked"

    match_frame.pack_forget()
    update_score_labels()
    scoring_frame.pack()

def update_score_labels():
    match = matches[current_match]
    team1_label.config(text=f"{match['team1_name']}: {match['team1_score']} points")
    team2_label.config(text=f"{match['team2_name']}: {match['team2_score']} points")

def add_points(team, points):
    if current_match is None:
        return

    if matches[current_match]["locked"] == "locked":
        messagebox.showerror("Error", "Cannot edit a locked match!")
        return

    if team == 1:
        matches[current_match]['team1_score'] += points
    elif team == 2:
        matches[current_match]['team2_score'] += points

    update_score_labels()

def end_match():
    if current_match is None:
        return

    lock = messagebox.askyesno("End Match", "Do you want to lock this match? (Prevent future edits)")
    if lock:
        matches[current_match]["locked"] = "locked"
    else:
        matches[current_match]["locked"] = "unlocked"

    save_matches()
    scoring_frame.pack_forget()
    match_frame.pack()

def create_new_match():
    match_name = simpledialog.askstring("New Match", "Enter match name:")
    if not match_name:
        return

    team1_name = simpledialog.askstring("Team 1", "Enter Team 1 name:")
    if not team1_name:
        return

    team2_name = simpledialog.askstring("Team 2", "Enter Team 2 name:")
    if not team2_name:
        return

    matches[match_name] = {
        "team1_name": team1_name,
        "team1_score": 0,
        "team2_name": team2_name,
        "team2_score": 0,
        "locked": "unlocked"
    }

    match_listbox.insert(tk.END, match_name)
    start_scoring(match_name)

def view_results():
    result_window = tk.Toplevel(root)
    result_window.title("Match Results")

    for match, data in matches.items():
        status = "🔒" if data["locked"] == "locked" else "🔓"
        info = f"{match}: {data['team1_name']} {data['team1_score']} - {data['team2_score']} {data['team2_name']} {status}"
        tk.Label(result_window, text=info, font=("Arial", 12)).pack(pady=2)

# GUI Setup
root = tk.Tk()
root.title("Tournament Scoring Program")

# Frame for match selection
match_frame = tk.Frame(root)

match_label = tk.Label(match_frame, text="Select a Match:", font=("Arial", 16))
match_label.pack(pady=10)

match_listbox = tk.Listbox(match_frame)
match_listbox.pack(pady=5)

start_button = tk.Button(match_frame, text="Start Selected Match", command=lambda: start_scoring(match_listbox.get(tk.ACTIVE)))
start_button.pack(pady=5)

new_match_button = tk.Button(match_frame, text="Create New Match", command=create_new_match)
new_match_button.pack(pady=5)

view_results_button = tk.Button(match_frame, text="View Results", command=view_results)
view_results_button.pack(pady=5)

match_frame.pack()

# Frame for scoring
scoring_frame = tk.Frame(root)

team1_label = tk.Label(scoring_frame, text="Team 1: 0 points", font=("Arial", 16))
team1_label.pack(pady=10)

team1_frame = tk.Frame(scoring_frame)
team1_frame.pack(pady=5)
tk.Button(team1_frame, text="+1", width=10, command=lambda: add_points(1, 1)).pack(side="left", padx=5)
tk.Button(team1_frame, text="+2", width=10, command=lambda: add_points(1, 2)).pack(side="left", padx=5)
tk.Button(team1_frame, text="+3", width=10, command=lambda: add_points(1, 3)).pack(side="left", padx=5)

team2_label = tk.Label(scoring_frame, text="Team 2: 0 points", font=("Arial", 16))
team2_label.pack(pady=10)

team2_frame = tk.Frame(scoring_frame)
team2_frame.pack(pady=5)
tk.Button(team2_frame, text="+1", width=10, command=lambda: add_points(2, 1)).pack(side="left", padx=5)
tk.Button(team2_frame, text="+2", width=10, command=lambda: add_points(2, 2)).pack(side="left", padx=5)
tk.Button(team2_frame, text="+3", width=10, command=lambda: add_points(2, 3)).pack(side="left", padx=5)

end_match_button = tk.Button(scoring_frame, text="End Match", command=end_match)
end_match_button.pack(pady=20)

# Load matches if file exists
load_matches()

root.mainloop()
