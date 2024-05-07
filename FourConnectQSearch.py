import numpy as np
import random
import matplotlib.pyplot as plt

class ConnectFour:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns), dtype=int)

    def drop_piece(self, column, piece):
        if not self.is_valid_location(column):
            return False
        for row in range(self.rows-1, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = piece
                return True
        return False

    def is_valid_location(self, column):
        return self.board[0][column] == 0

    def check_win(self, piece):
        # Check horizontal locations
        for c in range(self.columns-3):
            for r in range(self.rows):
                if self.board[r][c] == piece and all(self.board[r][c+i] == piece for i in range(1, 4)):
                    return True

        # Check vertical locations
        for c in range(self.columns):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and all(self.board[r+i][c] == piece for i in range(1, 4)):
                    return True

        # Check positively sloped diagonals
        for c in range(self.columns-3):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and all(self.board[r+i][c+i] == piece for i in range(1, 4)):
                    return True

        # Check negatively sloped diagonals
        for c in range(self.columns-3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and all(self.board[r-i][c+i] == piece for i in range(1, 4)):
                    return True

        return False

    def is_full(self):
        return all(self.board[0][c] != 0 for c in range(self.columns))

    def reset_board(self):
        self.board = np.zeros((self.rows, self.columns), dtype=int)

    def print_board(self):
        flipped_board = self.board
        print_board = np.where(flipped_board == 1, 'X', flipped_board)
        print_board = np.where(print_board == '-1', 'O', print_board)
        print_board = np.where(print_board == '0', '-', print_board)
        print(print_board)


class QLearningAgent:
    def __init__(self, game, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.q_table = {}  # Store Q-values as a dictionary {(state, action): value}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.game = game

    def get_state(self):
        return tuple(map(tuple, self.game.board))

    def choose_action(self):
        state = self.get_state()
        if random.random() < self.epsilon:  # Exploration
            return random.choice([c for c in range(self.game.columns) if self.game.is_valid_location(c)])
        
        q_values = [self.q_table.get((state, c), 0) for c in range(self.game.columns)]
        max_q = max(q_values) if q_values else float('-inf')
        actions = [c for c in range(self.game.columns) if q_values[c] == max_q and self.game.is_valid_location(c)]

        if not actions:  # Fallback if no valid actions based on Q-values
            actions = [c for c in range(self.game.columns) if self.game.is_valid_location(c)]
            if not actions:  # If no actions are possible, return None or raise an exception
                raise Exception("No valid moves available")

        return random.choice(actions)


    def update_q_table(self, state, action, reward, next_state, piece):
        current_q = self.q_table.get((state, action), 0)
        next_q = max(self.q_table.get((next_state, c), 0) for c in range(self.game.columns))

        # Evaluate future state using heuristic for the piece that just moved
        heuristic_reward = evaluate_board(self.game.board, piece)

        # Update rule incorporating heuristic evaluation
        self.q_table[(state, action)] = current_q + self.alpha * (reward + self.gamma * next_q + heuristic_reward - current_q)



def evaluate_board(board, piece):
    score = 0
    opp_piece = -piece

    # Score parameters
    three_in_row = 100
    two_in_row = 10
    one_in_row = 1

    # Directions: horizontal, vertical, diagonal /
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(6):
        for c in range(7):
            if board[r][c] == 0:
                # Temporarily play the piece on the board
                board[r][c] = piece
                for dr, dc in directions:
                    score += count_lines(board, r, c, dr, dc, piece) * three_in_row
                board[r][c] = opp_piece
                for dr, dc in directions:
                    score -= count_lines(board, r, c, dr, dc, opp_piece) * three_in_row
                # Reset the board
                board[r][c] = 0
    return score

def count_lines(board, row, col, dr, dc, piece):
    count = 0
    # Count 1-step in each direction
    for i in range(1, 4):
        if 0 <= row + dr*i < 6 and 0 <= col + dc*i < 7:
            if board[row + dr*i][col + dc*i] != piece:
                break
        count += 1
    return count


def train(agent, episodes=10000):
    # Metrics logging
    win_rates = []
    draw_rates = []
    average_game_lengths = []
    win_count = 0
    draw_count = 0
    total_moves = 0

    for episode in range(episodes):
        game_over = False
        game.reset_board()
        current_piece = 1  # Start with player 1

        while not game_over:
            state = agent.get_state()
            action = agent.choose_action()

            # Ensure valid move
            while not game.drop_piece(action, current_piece):
                action = agent.choose_action()  # Choose another action if not valid

            if game.check_win(current_piece):
                reward = 1  # Win
                game_over = True
            elif game.is_full():
                reward = 0.5  # Draw
                game_over = True
            else:
                reward = 0  # No immediate reward

            next_state = agent.get_state()

            # Update Q-table for the piece that just moved
            agent.update_q_table(state, action, reward, next_state, current_piece)

            # Switch player
            current_piece = -current_piece

            # Metrics calculation
            total_moves += 1

        if game.check_win(1):
            win_count += 1
        elif game.is_full():
            draw_count += 1

        # add for metrics plotting
        win_rates.append(win_count / (episode + 1))
        draw_rates.append(draw_count / (episode + 1))
        average_game_lengths.append(total_moves / (episode + 1))


        if (episode + 1) % 1000 == 0:
            print(f"Episode {episode + 1} completed.")
            print("Win Rate:", win_count / (episode + 1))
            print("Draw Rate:", draw_count / (episode + 1))
            print("Average Game Length:", total_moves / (episode + 1))


        if (episode + 1) % 1000 == 0:
            print(f"Episode {episode + 1} completed.")
        
    ## Plotting
    # Plotting and saving each metric separately
    episodes_range = range(1, episodes + 1)

    # Plot and save win rate
    plt.plot(episodes_range, win_rates)
    plt.xlabel('Episodes')
    plt.ylabel('Win Rate')
    plt.title('Win Rate over Episodes')
    plt.savefig('win_rate_plot.png')
    plt.close()

    # Plot and save draw rate
    plt.plot(episodes_range, draw_rates)
    plt.xlabel('Episodes')
    plt.ylabel('Draw Rate')
    plt.title('Draw Rate over Episodes')
    plt.savefig('draw_rate_plot.png')
    plt.close()

    # Plot and save average game length
    plt.plot(episodes_range, average_game_lengths)
    plt.xlabel('Episodes')
    plt.ylabel('Average Game Length')
    plt.title('Average Game Length over Episodes')
    plt.savefig('average_game_length_plot.png')
    plt.close()

    # Plotting win rate, draw rate and loss rate together
    plt.plot(episodes_range, win_rates, label='Win Rate')
    plt.plot(episodes_range, [1 - rate for rate in win_rates], label='Loss Rate')
    plt.plot(episodes_range, draw_rates, label='Draw Rate')
    plt.xlabel('Episodes')
    plt.ylabel('Rate/Length')
    plt.title('Performance Metrics over Episodes')
    plt.legend()
    plt.savefig('combined_metrics_plot.png')
    plt.close()



def play_game(agent, human=False):
    game.reset_board()
    game_over = False
    current_piece = 1

    while not game_over:
        if current_piece == 1 or not human:
            action = agent.choose_action()
            print("Agent's move:")
        else:
            valid = False
            while not valid:
                try:
                    action = int(input("Your move (0-6): "))
                    if not game.is_valid_location(action):
                        raise ValueError
                    valid = True
                except ValueError:
                    print("Invalid move. Try again.")

        game.drop_piece(action, current_piece)
        game.print_board()

        if game.check_win(current_piece):
            if current_piece == 1:
                print("Player 1 wins!" if human else "Agent wins!")
            else:
                print("Player 2 wins!")
            game_over = True
        elif game.is_full():
            print("It's a draw!")
            game_over = True

        current_piece = -current_piece

# Example usage
game = ConnectFour()
agent = QLearningAgent(game)
train(agent, episodes=9000)  # Train the agent

# Now decide if playing against the agent or let it play against itself
mode = input("Type 'human' to play against the agent, anything else to watch it play against itself: ").strip().lower()
play_game(agent, human=(mode == 'human'))