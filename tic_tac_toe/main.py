#!/usr/bin/env python3

import time
from game_logic import TicTacToe
from robot_control import RobotController

def setup_game():
    game = TicTacToe()
    robot = RobotController()
    robot.calibrate_workspace()
    return game, robot

def get_user_move(game):
    while True:
        try:
            move = int(input("Enter your move (1-9, top-left is 1, bottom-right is 9): ")) - 1
            if 0 <= move <= 8 and game.board[move // 3][move % 3] == 0:
                return move
            print("Invalid move! Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")

def main():
    game, robot = setup_game()
    print("Game starts! You are X, robot is O. Enter move (1-9).")
    
    while not game.check_winner() and not game.is_board_full():
        # User move
        user_move = get_user_move(game)
        row, col = user_move // 3, user_move % 3
        game.make_move(row, col, 'X')
        print(game)
        
        if game.check_winner():
            print("You win!")
            break
        if game.is_board_full():
            print("It's a draw!")
            break
        
        # Robot move
        print("Robot is thinking...")
        robot_move = game.get_best_move()
        row, col = robot_move // 3, robot_move % 3
        game.make_move(row, col, 'O')
        robot.pick_from_yard()  # Pick marker
        robot.place_at_position(robot_move)  # Place marker
        print(game)
        
        if game.check_winner():
            print("Robot wins!")
            break
    
    robot.close()

if __name__ == "__main__":
    main()