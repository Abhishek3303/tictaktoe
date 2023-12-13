from flask import Flask, render_template

app = Flask(__name__)

# Initialize game state variables
board = ['', '', '', '', '', '', '', '', '']
current_player = 'X'
is_game_active = True
score_x = 0
score_o = 0
score_draw = 0

winning_conditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

# Function to restart the game
def restart():
    global board, current_player, is_game_active, score_x, score_o, score_draw
    board = ['', '', '', '', '', '', '', '', '']
    is_game_active = True
    current_player = 'X'

# Route for the main game page
@app.route('/')
def index():
    return render_template('index.html', board=board, current_player=current_player)

# Route to handle user actions
@app.route('/user_action/<int:index>')
def user_action(index):
    global board, current_player, is_game_active

    if is_valid_action(index) and is_game_active:
        board[index] = current_player
        handle_result_validation()
        change_player()

    return render_template('game_status.html',
                           board=board,
                           current_player=current_player,
                           announcement=get_announcement(),
                           is_game_over=not is_game_active,
                           scoreboard=get_scoreboard())

# Route to reset the game board
@app.route('/reset_board')
def reset_board():
    global board, current_player, is_game_active, score_x, score_o, score_draw

    board = ['', '', '', '', '', '', '', '', '']
    is_game_active = True
    current_player = 'X'

    return render_template('game_status.html',
                           board=board,
                           current_player=current_player,
                           announcement="",
                           is_game_over=False,
                           scoreboard=get_scoreboard())

# Function to check if an action is valid
def is_valid_action(index):
    return board[index] == ''

# Function to switch the current player
def change_player():
    global current_player
    current_player = 'O' if current_player == 'X' else 'X'

# Function to get the game announcement
def get_announcement():
    global is_game_active

    for condition in winning_conditions:
        a, b, c = [board[i] for i in condition]
        if a == b == c and a != '':
            is_game_active = False
            restart()

    if '' not in board:
        is_game_active = False
        restart()

    return f'Player {current_player}\'s turn'

# Function to handle result validation
def handle_result_validation():
    global is_game_active, score_x, score_o, score_draw

    for condition in winning_conditions:
        a, b, c = [board[i] for i in condition]
        if a == b == c and a != '':
            is_game_active = False
            if a == 'X':
                score_x += 1
            elif a == 'O':
                score_o += 1
            restart()

    if '' not in board:
        is_game_active = False
        score_draw += 1
        restart()

# Function to get the current scoreboard
def get_scoreboard():
    global score_x, score_o, score_draw
    return f'Score: Player X - {score_x}, Player O - {score_o}, Draw - {score_draw}'

if __name__ == '__main__':
    app.run(debug=True)
