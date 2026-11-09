import time
import random
import os

# Grid dimensions
GRID_WIDTH = 20
GRID_HEIGHT = 10

# Characters for display
AMR_CHAR = '🤖'
TARGET_CHAR = '🎯'
OBSTACLE_CHAR = '🚧'
EMPTY_CHAR = ' . '

class AMR:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, target_x, target_y, obstacles):
        # Calculate potential moves (up, down, left, right)
        possible_moves = []
        if self.x < target_x: possible_moves.append((self.x + 1, self.y))
        if self.x > target_x: possible_moves.append((self.x - 1, self.y))
        if self.y < target_y: possible_moves.append((self.x, self.y + 1))
        if self.y > target_y: possible_moves.append((self.x, self.y - 1))

        # Simple heuristic: Manhattan distance to target
        def manhattan_distance(px, py, tx, ty):
            return abs(px - tx) + abs(py - ty)

        current_dist = manhattan_distance(self.x, self.y, target_x, target_y)
        best_move = (self.x, self.y) # Default: stay put if no better move found

        # Shuffle to add some non-determinism if multiple moves are equally good
        random.shuffle(possible_moves)

        for nx, ny in possible_moves:
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                # AMR's core concept: It senses its environment and avoids obstacles.
                if (nx, ny) not in obstacles:
                    new_dist = manhattan_distance(nx, ny, target_x, target_y)
                    if new_dist < current_dist: # Only move if it gets closer to target
                        best_move = (nx, ny)
                        break # Take the first valid closer move found

        self.x, self.y = best_move

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def move_randomly(self, grid_width, grid_height, forbidden_positions):
        # Try to move to a new random adjacent position, avoiding forbidden spots
        possible_adjacent_moves = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < grid_width and 0 <= ny < grid_height and \
               (nx, ny) not in forbidden_positions:
                possible_adjacent_moves.append((nx, ny))

        if possible_adjacent_moves:
            self.x, self.y = random.choice(possible_adjacent_moves)
        else:
            # If stuck, teleport to a completely new random free spot
            self.teleport_randomly(grid_width, grid_height, forbidden_positions)

    def teleport_randomly(self, grid_width, grid_height, forbidden_positions):
        while True:
            new_x = random.randint(0, grid_width - 1)
            new_y = random.randint(0, grid_height - 1)
            if (new_x, new_y) not in forbidden_positions:
                self.x, self.y = new_x, new_y
                break

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    amr = AMR(0, 0)
    target_x, target_y = GRID_WIDTH - 1, GRID_HEIGHT - 1
    obstacle = Obstacle(GRID_WIDTH // 2, GRID_HEIGHT // 2)

    print("AMR Simulation: Dynamic Obstacle Avoidance")
    print("🤖: AMR, 🎯: Target, 🚧: Obstacle")
    input("Press Enter to start...")

    step_count = 0
    while (amr.x, amr.y) != (target_x, target_y):
        clear_screen()
        step_count += 1

        # Get current positions of all entities
        amr_pos = (amr.x, amr.y)
        target_pos = (target_x, target_y)
        obstacle_pos = obstacle.get_position()

        # Display the grid
        for y in range(GRID_HEIGHT):
            row_chars = []
            for x in range(GRID_WIDTH):
                if (x, y) == amr_pos:
                    row_chars.append(AMR_CHAR)
                elif (x, y) == target_pos:
                    row_chars.append(TARGET_CHAR)
                elif (x, y) == obstacle_pos:
                    row_chars.append(OBSTACLE_CHAR)
                else:
                    row_chars.append(EMPTY_CHAR)
            print("".join(row_chars))

        print(f"\nStep: {step_count}")
        print(f"AMR Position: ({amr.x}, {amr.y})")
        print(f"Target Position: ({target_x}, {target_y})")
        print(f"Obstacle Position: ({obstacle.x}, {obstacle.y})")

        # AMR moves, considering the current obstacle position
        amr.move_towards(target_x, target_y, {obstacle_pos})

        # Obstacle moves dynamically every few steps, simulating a changing environment
        if step_count % 5 == 0:
            # Ensure the obstacle doesn't move onto the AMR or target
            forbidden_for_obstacle = {amr_pos, target_pos}
            obstacle.move_randomly(GRID_WIDTH, GRID_HEIGHT, forbidden_for_obstacle)

        time.sleep(0.3) # Pause for simulation speed

    clear_screen()
    print("".join([EMPTY_CHAR] * GRID_WIDTH)) # Print an empty line for spacing
    print(f"AMR reached the target in {step_count} steps!")
    print(f"Final AMR Position: ({amr.x}, {amr.y})")
    print(f"Target Position: ({target_x}, {target_y})")
    print("".join([EMPTY_CHAR] * GRID_WIDTH)) # Print an empty line for spacing

if __name__ == "__main__":
    main()
