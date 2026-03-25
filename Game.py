import tkinter as tk
import random
import time
import json

# -------- SPLASH --------
splash = tk.Tk()
splash.geometry("600x400")
splash.config(bg="#020617")

tk.Label(splash, text="🧠 MEMORY GAME",
         fg="#38bdf8", bg="#020617",
         font=("Segoe UI", 34, "bold")).pack(expand=True)

splash.update()
time.sleep(2)
splash.destroy()

# -------- MAIN --------
root = tk.Tk()
root.title("🔥 Memory Game Ultra 🔥")
root.geometry("950x750")
root.config(bg="#020617")

# -------- VARIABLES --------
cards = []
buttons = []
first = None
second = None
moves = 0
start_time = 0
current_level = 4
matched = set()   # ✅ NEW

emojis = ["🍎","🍌","🍇","🍒","🍍","🥝","🍉","🍑",
          "🚗","🚕","🚙","🚌","🏎️","🚓","🚑","🚒",
          "🐶","🐱","🐭","🐼","🐸","🐵","🦁","🐯"]

# -------- TOP --------
top = tk.Frame(root, bg="#020617")
top.pack(pady=15)

info = tk.Label(top, text="Moves: 0", fg="#38bdf8", bg="#020617",
                font=("Segoe UI", 16, "bold"))
info.grid(row=0, column=0, padx=30)

timer_label = tk.Label(top, text="Time: 0s", fg="#facc15", bg="#020617",
                       font=("Segoe UI", 16, "bold"))
timer_label.grid(row=0, column=1, padx=30)

best_label = tk.Label(top, text="Best: --", fg="#4ade80", bg="#020617",
                      font=("Segoe UI", 16, "bold"))
best_label.grid(row=0, column=2, padx=30)

# -------- TIMER --------
def update_timer():
    if start_time:
        timer_label.config(text=f"Time: {int(time.time()-start_time)}s")
    root.after(1000, update_timer)

# -------- FILE --------
def load_best():
    try:
        return json.load(open("leaderboard.json"))
    except:
        return []

def save_score(score):
    data = load_best()
    data.append(score)
    data = sorted(data)[:5]
    json.dump(data, open("leaderboard.json","w"))

# -------- FLIP ANIMATION --------
def flip_animation(btn, value):
    for size in range(18, 5, -3):
        btn.config(font=("Segoe UI", size))
        root.update()
        root.after(20)

    btn.config(text=value, bg="#22d3ee")

    for size in range(5, 18, 3):
        btn.config(font=("Segoe UI", size))
        root.update()
        root.after(20)

# -------- GAME --------
def on_click(i):
    global first, second, moves, start_time

    if buttons[i]["text"] != "" or second:
        return

    if start_time == 0:
        start_time = time.time()

    flip_animation(buttons[i], cards[i])

    if first is None:
        first = i
    else:
        second = i
        moves += 1
        info.config(text=f"Moves: {moves}")
        root.after(400, check_match)

def check_match():
    global first, second, matched

    if cards[first] != cards[second]:
        for b in [buttons[first], buttons[second]]:
            b.config(bg="#ef4444")
        root.update()
        root.after(200)

        for b in [buttons[first], buttons[second]]:
            b.config(text="", bg="#1e293b", font=("Segoe UI", 18))
    else:
        buttons[first].config(bg="#22c55e", state="disabled")
        buttons[second].config(bg="#22c55e", state="disabled")

        matched.add(first)
        matched.add(second)

    first = None
    second = None
    check_win()

def check_win():
    for btn in buttons:
        if btn["text"] == "":
            return

    elapsed = int(time.time() - start_time)
    save_score(moves)

    win = tk.Toplevel(root)
    win.geometry("400x320")
    win.config(bg="#020617")

    tk.Label(win, text="🎉 YOU WON!",
             fg="#facc15", bg="#020617",
             font=("Segoe UI", 22, "bold")).pack(pady=10)

    tk.Label(win, text=f"Moves: {moves}", fg="white", bg="#020617").pack()
    tk.Label(win, text=f"Time: {elapsed}s", fg="white", bg="#020617").pack()

    tk.Label(win, text="🏆 Leaderboard",
             fg="#38bdf8", bg="#020617",
             font=("Segoe UI", 14)).pack(pady=10)

    for s in load_best():
        tk.Label(win, text=f"{s} moves", fg="white", bg="#020617").pack()

    tk.Button(win, text="Play Again",
              bg="#38bdf8", fg="black",
              command=lambda:[win.destroy(), start_game(current_level)]
              ).pack(pady=10)

# -------- START --------
def start_game(level):
    global cards, buttons, first, second, moves, start_time, current_level, matched

    current_level = level
    first = second = None
    moves = 0
    start_time = 0
    matched = set()   # ✅ RESET
    info.config(text="Moves: 0")

    for widget in frame.winfo_children():
        widget.destroy()

    size = level
    total = size * size
    pairs = total // 2

    values = emojis[:pairs] * 2
    random.shuffle(values)
    cards = values

    buttons.clear()

    for i in range(total):
        btn = tk.Button(frame, text="",
                        width=7, height=3,
                        font=("Segoe UI", 18, "bold"),
                        bg="#1e293b", fg="white",
                        relief="flat",
                        activebackground="#334155",
                        command=lambda i=i: on_click(i))

        # ✅ SAFE HOVER (IGNORE MATCHED)
        btn.bind("<Enter>", lambda e, b=btn, i=i:
                 b.config(bg="#334155") if i not in matched else None)

        btn.bind("<Leave>", lambda e, b=btn, i=i:
                 b.config(bg="#1e293b") if i not in matched else None)

        btn.grid(row=i//size, column=i%size, padx=8, pady=8)
        buttons.append(btn)

# -------- UI --------
frame = tk.Frame(root, bg="#020617")
frame.pack(pady=20)

btns = tk.Frame(root, bg="#020617")
btns.pack(pady=10)

def nice_btn(text, color, cmd):
    return tk.Button(btns, text=text,
                     bg=color, fg="black",
                     font=("Segoe UI", 12, "bold"),
                     width=12, height=2,
                     command=cmd)

nice_btn("Easy", "#22c55e", lambda: start_game(4)).grid(row=0, column=0, padx=10)
nice_btn("Medium", "#facc15", lambda: start_game(6)).grid(row=0, column=1, padx=10)
nice_btn("Hard", "#ef4444", lambda: start_game(8)).grid(row=0, column=2, padx=10)

tk.Button(root, text="Restart 🔄",
          bg="#38bdf8", fg="black",
          font=("Segoe UI", 12, "bold"),
          command=lambda: start_game(current_level)).pack(pady=15)

# -------- INIT --------
start_game(4)
update_timer()

root.mainloop()