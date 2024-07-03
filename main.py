from tkinter import *
from tkinter import simpledialog, messagebox
import random
import time

def restart():
    global player, player1_wins, player2_wins
    # Updates the player order and text bar
    player = random.choice(characters)
    label.config(text=f"{get_player_name(player)}'s Turn")
    # Updates button text to blank spaces and resets button colors
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", fg="black", bg="SystemButtonFace")
    check_winner()

def next_turn(row, column):
    global player, player1_wins, player2_wins
    if buttons[row][column]['text'] == "" and check_winner() is False:
        if player == characters[0]:
            buttons[row][column].config(text=player, fg="white", bg="blue")
        else:
            buttons[row][column].config(text=player, fg="white", bg="red")
        
        if check_winner() is False:
            player = characters[1] if player == characters[0] else characters[0]
            label.config(text=f"{get_player_name(player)}'s Turn")
        elif check_winner() is True:
            highlight_winner()
            if player == characters[0]:
                player1_wins += 1
            else:
                player2_wins += 1
            update_scores()
            show_party_effect(f"{get_player_name(player)} Wins!")
        elif check_winner() == "Tie":
            label.config(text="It's a Tie!")

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != '':
            return True
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != '':
            return True
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        return True
    if buttons[2][0]['text'] == buttons[1][1]['text'] == buttons[0][2]['text'] != '':
        return True
    if empty_spaces() is False:
        return "Tie"
    return False

def highlight_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != '':
            for column in range(3):
                buttons[row][column].config(bg="green")
            return
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != '':
            for row in range(3):
                buttons[row][column].config(bg="green")
            return
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        for i in range(3):
            buttons[i][i].config(bg="green")
        return
    if buttons[2][0]['text'] == buttons[1][1]['text'] == buttons[0][2]['text'] != '':
        for i in range(3):
            buttons[2-i][i].config(bg="green")
        return

def empty_spaces():
    spaces = 9
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != '':
                spaces -= 1
    if spaces == 0:
        return False
    return True

def ask_player_names():
    global player1_name, player2_name
    while True:
        player1_name = simpledialog.askstring("Player 1", "Enter the name of Player 1 (X):")
        if player1_name and len(player1_name) >= 3:
            break
        else:
            messagebox.showerror("Invalid Name", "Player name must be at least 3 characters long.")
    
    while True:
        player2_name = simpledialog.askstring("Player 2", "Enter the name of Player 2 (O):")
        if player2_name and len(player2_name) >= 3:
            break
        else:
            messagebox.showerror("Invalid Name", "Player name must be at least 3 characters long.")
    
    label.config(text=f"{get_player_name(player)}'s Turn")

def get_player_name(char):
    if char == "x":
        return f"{player1_name} (X)"
    else:
        return f"{player2_name} (O)"

def change_players():
    ask_player_names()
    restart()

def update_scores():
    score_label.config(text=f"{player1_name}: {player1_wins}   {player2_name}: {player2_wins}")

def show_party_effect(message):
    # Create a new window for party effect
    party_window = Toplevel(board)
    party_window.title("Party Time!")
    party_window.configure(bg="black")
    party_window.geometry("400x300")
    
    # Display the winning message
    win_label = Label(party_window, text=message, font=("futura", 30), fg="white", bg="black")
    win_label.pack(pady=50)
    
    # Party bomb effect with changing colors
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    for _ in range(20):
        for color in colors:
            win_label.config(fg=color)
            party_window.update()
            time.sleep(0.1)
    
    # Destroy the party window after the effect
    party_window.destroy()
    
    # Restart the game automatically
    restart()

board = Tk()
board.title("Tic-Tac-Toe")

characters = ["x", "o"]
player = random.choice(characters)
player1_name = ""
player2_name = ""
player1_wins = 0
player2_wins = 0

buttons = [['', '', ''],
           ['', '', ''],
           ['', '', '']]

label = Label(text=f"{player}'s Turn", font=("futura", 40))
label.pack(side="top")

new_game_button = Button(text="Restart", font=("futura", 20), command=restart, fg="white", bg="green")
new_game_button.pack(side="top")

frame = Frame(board)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=('consolas', 40), width=5, height=2, command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

footer = Label(text="Tic Tac Toe", font=("futura", 20))
footer.pack(side="bottom")

change_players_button = Button(text="Change Players", font=("futura", 20), command=change_players, fg="white", bg="blue")
change_players_button.pack(side="bottom")

score_label = Label(board, text="", font=("futura", 16))
score_label.pack(side="right")
update_scores()

board.after(100, ask_player_names)  # Ask for player names after the main loop starts

board.mainloop()
