import pygame
import random

class Overworld:
    def __init__(self) -> None:
        # Use subclasses to define different size
        self.rows, self.cols = 1, 1
        # Create Overworld grid:
        self.overworld_grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

        # Colors
        self.colors = {
            'L': (0, 0, 255),   # Blue for lake
            'R': (0, 255, 0),   # Green for river
            'C': (255, 0, 0),   # Red for combat
            'S': (255, 255, 0), # Yellow for non-combat
            'V': (255, 0, 255), # Magenta for victory
            'P': (0, 255, 255)  # Cyan for player
        }

        # Define lake & river frequency values
        self.lake_frequency = 1
        self.river_frequency = 1

        # Define lake radius range
        self.lake_radius_min = 3
        self.lake_radius_max = 5

        # Define lake coverage range
        self.lake_coverage_min = 10
        self.lake_coverage_max = 10

        # Define river coverage range
        self.river_coverage_min = 5
        self.river_coverage_max = 10

        # Define combat & noncombat encoutners max
        self.combat_encounters_max = 5
        self.noncombat_encounters_max = 5

        # Define how far player can spawn from edge
        self.player_spawn_limit = 2

        # Set up display
        self.tile_size = 20
        self.screen = pygame.display.set_mode((self.cols * self.tile_size, self.rows * self.tile_size))
        pygame.display.set_caption('Overworld')

    def generate_terrain_features(self):
        self.generate_lakes()
        self.generate_rivers()
    
    def generate_lakes(self):
        # Lakes should gen near edges and center
        while True:
            tmp_grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.is_near_lake(tmp_grid, row, col, 2):
                        continue

                    distance_to_center = abs(self.rows // 2 - row) + abs(self.cols // 2 - col)
                    distance_to_edge = min(row, col, self.rows - 1 - row, self.cols - 1 - col)

                    weight_center = (max(self.rows // 2, self.cols // 2) - distance_to_center) / max(self.rows // 2, self.cols // 2)
                    weight_edge = distance_to_edge / max(self.rows // 2, self.cols // 2)

                    weight = (weight_center + weight_edge) / 2
                    probability = weight * self.lake_frequency * 0.5  # Adjusted the probability multiplier

                    if random.random() < probability:
                        lake_radius = random.randint(self.lake_radius_min, self.lake_radius_max)
                        self.place_lake(tmp_grid, row, col, lake_radius)

            if self.lake_coverage_min < self.calculate_lake_coverage(tmp_grid) <= self.lake_coverage_max:
                self.overworld_grid = tmp_grid
                break

    
    def is_near_lake(self, grid, row, col, distance):
        for row_offset in range(-distance, distance + 1):
            for col_offset in range(-distance, distance + 1):
                new_row = row + row_offset
                new_col = col + col_offset
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    if 'L' in grid[new_row][new_col]:
                        return True
        return False

    def place_lake(self, grid, center_row, center_col, lake_radius):
        for row_offset in range(-lake_radius, lake_radius + 1):
            for col_offset in range(-lake_radius, lake_radius + 1):
                new_row = center_row + row_offset
                new_col = center_col + col_offset
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    grid[new_row][new_col].append('L')

    def calculate_lake_coverage(self, grid):
        lake_tiles = sum(['L' in cell for row in grid for cell in row])
        total_tiles = self.rows * self.cols
        return (lake_tiles / total_tiles) * 100
    
    def generate_rivers(self):
        # Rivers should start near edges and near lakes
        while True:
            tmp_grid = [[cell.copy() for cell in row] for row in self.overworld_grid]
            for row in range(self.rows):
                for col in range(self.cols):
                    if random.random() < self.river_frequency:
                        distance_to_edge = min(row, col, self.rows - 1 - row, self.cols - 1 - col)
                        weight_edge = distance_to_edge / max(self.rows // 2, self.cols // 2)
                        weight_lake = 1 if self.is_near_lake(tmp_grid, row, col, 2) else 0
                        weight = (weight_edge + weight_lake) / 2
                        if random.random() < weight:
                            self.place_river(tmp_grid, row, col)

            if self.river_coverage_min < self.calculate_river_coverage(tmp_grid) <= self.river_coverage_max:
                self.overworld_grid = tmp_grid
                break
    
    def place_river(self, grid, start_row, start_col):
        # Picks a random direction and decreases probability of river extending each time it extends
        row, col = start_row, start_col
        direction = random.choice(['up', 'down', 'left', 'right'])
        probability = 1.0

        while probability > 0.1:
            if 'L' not in grid[row][col]:
                grid[row][col].append('R')

            if direction == 'up':
                row -= 1
            elif direction == 'down':
                row += 1
            elif direction == 'left':
                col -= 1
            elif direction == 'right':
                col += 1

            if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                break

            if random.random() > probability:
                direction = random.choice(['up', 'down', 'left', 'right'])

            probability *= 0.9

    def calculate_river_coverage(self, grid):
        river_tiles = sum(['R' in cell for row in grid for cell in row])
        total_tiles = self.rows * self.cols
        return (river_tiles / total_tiles) * 100
    
    def generate_combat_encounters(self):
        # Combat encounters should not be placed on Lake/River tiles & weighted towards center
        # Create a temporary grid for placing combat encounters
        tmp_grid = [[cell.copy() for cell in row] for row in self.overworld_grid]
        
        # Function to calculate weighted probability for center of the map
        def center_weight(row, col):
            center_row, center_col = self.rows // 2, self.cols // 2
            dist = ((row - center_row) ** 2 + (col - center_col) ** 2) ** 0.5
            max_dist = ((self.rows // 2) ** 2 + (self.cols // 2) ** 2) ** 0.5
            return 1 - (dist / max_dist)

        # Generate combat encounters
        for _ in range(self.combat_encounters_max):
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)

                # Random probability weighted towards the center
                if random.random() < center_weight(row, col):
                    if 'L' not in tmp_grid[row][col] and 'R' not in tmp_grid[row][col] and 'C' not in tmp_grid[row][col]:
                        # TODO: Append randomized CPUSlangers instead of 'C'
                        tmp_grid[row][col].append('C')
                        break
        
        # Save the temporary grid to self.overworld_grid
        self.overworld_grid = tmp_grid
    
    def generate_noncombat_encounters(self):
        # Noncombat encounters weighted towards lakes and rivers
        # Create a temporary grid for placing non-combat encounters
        tmp_grid = [[cell.copy() for cell in row] for row in self.overworld_grid]
        
        # Function to calculate weighted probability based on proximity to lakes and rivers
        def proximity_weight(row, col):
            # Initialize weight
            weight = 0

            # Check proximity to lakes
            for r in range(max(0, row - 2), min(self.rows, row + 3)):
                for c in range(max(0, col - 2), min(self.cols, col + 3)):
                    if 'L' in tmp_grid[r][c]:
                        weight += 0.5  # Increment weight based on proximity to lakes
            
            # Check proximity to rivers
            for r in range(max(0, row - 2), min(self.rows, row + 3)):
                for c in range(max(0, col - 2), min(self.cols, col + 3)):
                    if 'R' in tmp_grid[r][c]:
                        weight += 0.5  # Increment weight based on proximity to rivers

            # Ensure weight is capped between 0 and 1
            return min(weight, 1)

        # Generate non-combat encounters
        for _ in range(self.noncombat_encounters_max):
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)

                # Random probability weighted by proximity to lakes and rivers
                if random.random() < proximity_weight(row, col):
                    if 'L' not in tmp_grid[row][col] and 'R' not in tmp_grid[row][col] and 'C' not in tmp_grid[row][col] and 'S' not in tmp_grid[row][col]:
                        # TODO: Append different encounters instead of just 'S'
                        tmp_grid[row][col].append('S')
                        break
        
        # Save the temporary grid to self.overworld_grid
        self.overworld_grid = tmp_grid

    def generate_victory_encounter(self):
        # Should place as close to center as possible
        # Calculate the center of the map
        center_row = self.rows // 2
        center_col = self.cols // 2

        # List of potential locations to try
        locations = [(center_row, center_col)]

        # Add surrounding tiles to the list
        for d in range(1, max(self.rows, self.cols)):
            for dr in [-d, d]:
                for dc in [-d, d]:
                    r, c = center_row + dr, center_col + dc
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        locations.append((r, c))
            if len(locations) > self.rows * self.cols:  # Avoid too many locations
                break

        # Sort locations by distance to the center, ensuring closer tiles are tried first
        locations.sort(key=lambda x: (abs(x[0] - center_row) + abs(x[1] - center_col)))

        # Attempt to place 'V'
        for r, c in locations:
            if not self.overworld_grid[r][c]:  # Ensure the tile is not occupied
                # TODO: Append a CPU BossSlanger instead of just 'V'
                self.overworld_grid[r][c].append('V')
                break

    def spawn_player(self):
        # Spawn on Random edge tile
        edge_tiles = [(row, col) for row in range(self.rows) for col in range(self.cols)
                      if self.is_edge_tile(row, col) and not self.overworld_grid[row][col]]
        
        if not edge_tiles:
            raise ValueError("No valid edge tiles available for player spawn.")
        
        # Choose a random tile from the available edge tiles
        chosen_tile = random.choice(edge_tiles)
        
        # Place the player
        row, col = chosen_tile
        # TODO: Append PlayerSlanger object instead of just 'P'
        self.overworld_grid[row][col] = 'P'

        print(f"Player spawned at ({row}, {col})")
    
    def is_edge_tile(self, row, col):
        return (row < self.player_spawn_limit or row >= self.rows - self.player_spawn_limit or
                col < self.player_spawn_limit or col >= self.cols - self.player_spawn_limit)

    def print_grid(self):
        for row in self.overworld_grid:
            print("".join(['L' if 'L' in cell 
                           else 'R' if 'R' in cell 
                           else 'C' if 'C' in cell 
                           else 'S' if 'S' in cell 
                           else 'V' if 'V' in cell 
                           else 'P' if 'P' in cell
                           else '.' for cell in row]))
    
    def draw_overworld(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw grid
        for row in range(self.rows):
            for col in range(self.cols):
                tile_list = self.overworld_grid[row][col]
                if tile_list:
                    # Use the first non-empty tile feature for color (if any)
                    tile = next((t for t in tile_list if t in self.colors), '.')
                    color = self.colors.get(tile, (255, 255, 255))  # Default to white if tile type is unknown
                    pygame.draw.rect(self.screen, color, (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))

        # Update display
        pygame.display.flip()

        
    def quit(self):
        pygame.quit()

class Desolate(Overworld):
    def __init__(self) -> None:
        super().__init__()
        self.rows, self.cols = 20, 50
        # Create Overworld grid:
        self.overworld_grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]

        # Define lake & river frequency values
        self.lake_frequency = 0.02
        self.river_frequency = 0.02

        # Define lake radius range
        self.lake_radius_min = 1
        self.lake_radius_max = 3

        # Define lake coverage range
        self.lake_coverage_min = 2
        self.lake_coverage_max = 15

        # Define river coverage range
        self.river_coverage_min = 5
        self.river_coverage_max = 15

        # Define max combat & noncombat encounters
        self.combat_encounters_max = 8
        self.noncombat_encounters_max = 10

        # Define how far player can spawn from edge
        self.player_spawn_limit = 2

        # Set up display
        self.tile_size = 20
        self.screen = pygame.display.set_mode((self.cols * self.tile_size, self.rows * self.tile_size))
        pygame.display.set_caption('Desolate')
