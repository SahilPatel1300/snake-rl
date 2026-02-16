from game import SnakeGameAI

def main():
    game = SnakeGameAI()
    # get user input for action 
    
    while True:
        user_input = input("Enter action (w: straight, d: right, a: left): ")
        if user_input == 'w':
            action = [1, 0, 0]
        elif user_input == 'd':
            action = [0, 1, 0]
        elif user_input == 'a':
            action = [0, 0, 1]
        reward, game_over, score = game.play_step(action=action)
        if game_over:
            break


if __name__ == "__main__":
    main()
