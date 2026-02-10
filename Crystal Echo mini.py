import random
import os
import time


class CrystalEcho:
    def __init__(self):
        self.width = 10
        self.height = 5
        self.player_x, self.player_y = 2, 2
        self.energy = 20
        self.crystals = 0
        self.cave = self.generate_cave()
        self.game_over = False
        self.score = 0

    def generate_cave(self):
        cave = [['.' for _ in range(self.width)] for _ in range(self.height)]
        # Place crystals and hazards procedurally
        for _ in range(3):
            x, y = random.randint(1, self.width - 2), random.randint(0, self.height - 1)
            cave[y][x] = 'C'  # Crystal
        for _ in range(2):
            x, y = random.randint(1, self.width - 2), random.randint(0, self.height - 1)
            cave[y][x] = 'H'  # Hazard (cave-in risk)
        return cave

    def print_cave(self, revealed=False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== CRYSTAL ECHO ===")
        print(f"Energy: {self.energy} | Crystals: {self.crystals}/5 | Score: {self.score}")
        print("w=forward, a/d=scan left/right, e=echo (reveals area, costs 2 energy)")

        for y in range(self.height):
            row = ''
            for x in range(self.width):
                if x == self.player_x and y == self.player_y:
                    row += 'P '
                elif revealed and self.cave[y][x] != '.':
                    row += self.cave[y][x] + ' '
                else:
                    row += '? '
            print(row)
        print()

    def move(self, dx, dy):
        new_x, new_y = self.player_x + dx, self.player_y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.player_x, self.player_y = new_x, new_y
            self.energy -= 1
            self.check_collisions()
            return True
        return False

    def scan(self, direction):
        self.energy -= 1
        print(f"Echo scan {direction}: Patterns shift nearby...")

    def echo(self):
        if self.energy >= 2:
            self.energy -= 2
            self.score += 10
            print("FULL ECHO! Crystals glow brighter.")
            return True
        print("Not enough energy!")
        return False

    def check_collisions(self):
        cell = self.cave[self.player_y][self.player_x]
        if cell == 'C':
            self.crystals += 1
            self.cave[self.player_y][self.player_x] = '.'
            self.score += 50
            print("Crystal collected! +50 score")
            time.sleep(0.5)
        elif cell == 'H':
            self.energy -= 5
            self.score -= 20
            print("Cave-in! Energy drained.")
            time.sleep(0.5)

    def run(self):
        while not self.game_over and self.energy > 0 and self.crystals < 5:
            self.print_cave(revealed=(self.echo_active if hasattr(self, 'echo_active') else False))

            cmd = input("Command: ").lower()
            if cmd == 'q':
                self.game_over = True
            elif cmd == 'w':
                self.move(1, 0)
            elif cmd == 'a':
                self.scan("left")
            elif cmd == 'd':
                self.scan("right")
            elif cmd == 'e':
                self.echo_active = self.echo()
            else:
                print("Invalid: w/a/d/e/q")

            if self.crystals >= 5:
                print("VICTORY! All crystals echo eternally.")
                break
            if self.energy <= 0:
                print("Energy depleted. Cave claims you.")

        print(f"Final Score: {self.score}")


if __name__ == "__main__":
    game = CrystalEcho()
    game.run()
