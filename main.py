import tkinter as tk
from tkinter import messagebox
import config

# Function to start the game
def start_game():
    hide_main_menu()
    show_game_interface()
    reset_game()

# Function to show the rules
def show_rules():
    hide_main_menu()
    message_label.config(
        text=f"Game Rules:\n"
             f"1. Guess the number.\n"
             f"2. The number consists of {config.riddle_length} digits.\n"
             f"3. Each digit is unique.\n"
             f"4. 'B' - correct digit in the correct place.\n"
             f"5. 'C' - correct digit in the wrong place.\n"
             f"6. You have a limited number of attempts.")
    message_label.pack(pady=20)
    back_button.pack(side="bottom", pady=10)

# Function to show the settings
def show_settings():
    hide_main_menu()
    message_label.config(text="Settings:")
    message_label.pack(pady=10)

    riddle_length_label.pack(pady=5)
    riddle_length_entry.pack(pady=5)
    unique_digits_label.pack(pady=5)
    unique_digits_check.pack(pady=5)
    difficulty_label.pack(pady=5)
    difficulty_menu.pack(pady=5)

    save_settings_button.pack(pady=10)
    back_button.pack(side="bottom", pady=10)

# Function to save the settings
def save_settings():
    try:
        new_riddle_length = int(riddle_length_entry.get())
        new_unique_digits = unique_digits_var.get() == 1
        new_difficulty = difficulty_var.get()
    except ValueError:
        messagebox.showerror("Error", "Enter correct values.")
        return

    with open('config.py', 'w') as config_file:
        config_file.write(f"riddle_length = {new_riddle_length}\n")
        config_file.write(f"unique_digits = {new_unique_digits}\n")
        config_file.write(f"difficulty = '{new_difficulty}'\n")

    messagebox.showinfo("Saved", "Settings successfully saved.")

# Function to exit the game
def exit_game():
    root.destroy()

# Function to go back to the main menu
def back_to_menu():
    hide_game_interface()
    hide_win_screen()
    hide_settings_menu()
    show_main_menu()

# Function to hide the main menu buttons
def hide_main_menu():
    start_button.pack_forget()
    rules_button.pack_forget()
    settings_button.pack_forget()
    exit_button.pack_forget()

# Function to show the main menu buttons
def show_main_menu():
    start_button.pack(pady=10)
    rules_button.pack(pady=10)
    settings_button.pack(pady=10)
    exit_button.pack(pady=10)

# Function to hide the game interface widgets
def hide_game_interface():
    entry.pack_forget()
    submit_button.pack_forget()
    attempts_label.pack_forget()
    results_label.pack_forget()
    attempts_list.pack_forget()
    results_list.pack_forget()
    back_button.place_forget()
    remaining_attempts_label.place_forget()

# Function to hide the settings menu widgets
def hide_settings_menu():
    riddle_length_label.pack_forget()
    riddle_length_entry.pack_forget()
    unique_digits_label.pack_forget()
    unique_digits_check.pack_forget()
    difficulty_label.pack_forget()
    difficulty_menu.pack_forget()
    save_settings_button.pack_forget()
    back_button.pack_forget()

# Function to show the game interface
def show_game_interface():
    message_label.config(text="Enter your guess:")
    message_label.pack(pady=10)
    remaining_attempts_label.place(x = 260, y = 125, anchor='ne')
    entry.pack(pady=5)
    submit_button.pack(pady=5)
    attempts_label.pack(side="left", padx=10)
    results_label.pack(side="right", padx=10)
    attempts_list.pack(side="left", padx=10)
    results_list.pack(side="right", padx=10)
    back_button.place(x=260, y=350, anchor='ne')

# Function to show the win screen
def show_win_screen():
    hide_game_interface()
    message_label.config(text="You won!", font=("Helvetica", 20, "bold"))
    message_label.pack(pady=20)
    play_again_button.pack(pady=10)
    back_button.pack(pady=10)

# Function to show the loss screen
def show_loss_screen():
    hide_game_interface()
    message_label.config(text="You lost!", font=("Helvetica", 20, "bold"))
    message_label.pack(pady=20)
    play_again_button.pack(pady=10)
    back_button.pack(pady=10)

# Function to submit the answer
def submit_answer():
    answer = entry.get()
    if len(answer) != config.riddle_length or not answer.isdigit():
        messagebox.showerror("Error", f"Enter a correct {config.riddle_length}-digit number.")
        return

    attempts.append(answer)
    result = check_answer(answer)
    results.append(result)
    update_results()

    if result == f"{config.riddle_length}B0C":
        show_win_screen()
    else:
        global remaining_attempts
        remaining_attempts -= 1
        update_remaining_attempts()
        if remaining_attempts <= 0:
            show_loss_screen()

# Function to reset the game
def reset_game():
    global attempts, results, riddle, max_attempts, remaining_attempts
    attempts = []
    results = []
    riddle = generate_riddle()
    difficulty = config.difficulty
    max_attempts = {"easy": 10, "medium": 8, "hard": 5}[difficulty]
    remaining_attempts = max_attempts
    update_remaining_attempts()
    update_results()

# Function to update the remaining attempts label
def update_remaining_attempts():
    remaining_attempts_label.config(text=f"Remaining attempts: {remaining_attempts}")

# Function to generate a random riddle
def generate_riddle():
    import random
    digits = list("0123456789")
    random.shuffle(digits)
    riddle = ''.join(digits[:config.riddle_length])
    if not config.unique_digits:
        while len(set(riddle)) != config.riddle_length or riddle[0] == '0':
            random.shuffle(digits)
            riddle = ''.join(digits[:config.riddle_length])
    return riddle

# Function to check the answer and return the result
def check_answer(answer):
    B = 0
    C = 0
    riddle_unmatched = []
    attempt_unmatched = []

    for i in range(config.riddle_length):
        if answer[i] == riddle[i]:
            B += 1
        else:
            riddle_unmatched.append(riddle[i])
            attempt_unmatched.append(answer[i])

    for char in attempt_unmatched:
        if char in riddle_unmatched:
            C += 1
            riddle_unmatched.remove(char)
    return f"{B}B{C}C"

# Function to update the results in the listboxes
def update_results():
    attempts_list.delete(0, tk.END)
    results_list.delete(0, tk.END)
    for attempt, result in zip(attempts, results):
        attempts_list.insert(tk.END, attempt)
        results_list.insert(tk.END, result)
    attempts_list.yview(tk.END)
    results_list.yview(tk.END)

# Function to play again
def play_again():
    hide_win_screen()
    start_game()

# Function to hide the win screen widgets
def hide_win_screen():
    message_label.pack_forget()
    play_again_button.pack_forget()
    back_button.pack_forget()

# Initialize variables
attempts = []
results = []
riddle = generate_riddle()

# Create the main window
root = tk.Tk()
root.title("Bulls and Cows")
root.geometry("400x400")

# Create buttons
start_button = tk.Button(root, text="Start Game", command=start_game)
rules_button = tk.Button(root, text="Rules", command=show_rules)
settings_button = tk.Button(root, text="Settings", command=show_settings)
exit_button = tk.Button(root, text="Exit Game", command=exit_game)
back_button = tk.Button(root, text="Back to Main Menu", command=back_to_menu)
submit_button = tk.Button(root, text="Submit", command=submit_answer)
play_again_button = tk.Button(root, text="Play Again", command=play_again)
save_settings_button = tk.Button(root, text="Save", command=save_settings)

# Create a label for displaying messages
message_label = tk.Label(root, text="", wraplength=300)

# Create labels and listboxes for displaying attempts and results
attempts_label = tk.Label(root, text="Attempts")
results_label = tk.Label(root, text="Results")
attempts_list = tk.Listbox(root)
results_list = tk.Listbox(root)

# Create an entry field for input
entry = tk.Entry(root)

# Settings fields
riddle_length_label = tk.Label(root, text="Riddle Length")
riddle_length_entry = tk.Entry(root)
riddle_length_entry.insert(0, config.riddle_length)

unique_digits_label = tk.Label(root, text="Unique Digits")
unique_digits_var = tk.IntVar(value=1 if config.unique_digits else 0)
unique_digits_check = tk.Checkbutton(root, variable=unique_digits_var)

difficulty_label = tk.Label(root, text="Difficulty")
difficulty_var = tk.StringVar(value=config.difficulty)
difficulty_menu = tk.OptionMenu(root, difficulty_var, "easy", "medium", "hard")

# Label for remaining attempts
remaining_attempts_label = tk.Label(root, text="")

# Place buttons on the main screen
start_button.pack(pady=10)
rules_button.pack(pady=10)
settings_button.pack(pady=10)
exit_button.pack(pady=10)

# Start the main event loop
root.mainloop()
