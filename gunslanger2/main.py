import pygame
from combat_stage import CombatStage
from slanger import PlayerSlanger, CPUSlanger
from overworld import Desolate

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# Clock to control the frame rate
CLOCK = pygame.time.Clock()

def main():
    print("Welcome gunslanger")

    # Overworld
    current_ow = Desolate()
    current_ow.generate_terrain_features()
    current_ow.generate_combat_encounters()
    current_ow.generate_noncombat_encounters()
    current_ow.generate_victory_encounter()
        # Generate Map:
            # Grid 40x40 (Or circle with r=40)
            # Generate random obsticals
                # Rivers
                # Lakes
                # Buildings
            # Generate combat encoutners
            # Generate non-combat encounters
            # Generate victory condition encounter
    # Spawn player
    player = PlayerSlanger()
    current_ow.spawn_player()
    # Draw overworld
    current_ow.draw_overworld()
        # Handle player movement:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Player enters combat tile:
                # Enter combat phase
            # Player enters non-combat tile:
                # Opens shop menu
    current_ow.quit()

    # Combat phase:
    # Generate combat stage
    combat_stage = CombatStage() # Generates 3x7
            # Generate random obsticals
    
    # Initialize opponent(s)
        # Quickdraw mini-game
            # Winner gets first move
        # First turn (Assume human player)
            # Player may move, shoot, load chamber, remove from chamber, "rotate" chamber
        # Second turn (Assume CPU player(s))
            # If there is a bullet in CPU players lane that will hit them, move.
            # If chamber has any bullets, shoot.
            # If chamber has no bullets, load until they have to move.
        # Bullet movement
            # Multiple bullets can be contained in same tile
            # Check if bullet has already hit a specific bullet in this movement phase.
                # bullets should not deal/take damage from the same bullet 2x in one turn
        # If either or both players die:
            # Surviving player wins, ties count as loss for human player
            # Assuming human player, calculate rewards
                # CPU players should drop some gold & a small amount of bullets
            # Show rewards menu (if human player wins)
                # When exited, return to Overworld.
            # Show new game options (if human player loses)

    # Button for "Chamber" menu (always visible)
        # When opened:
            # Show current Chamber in center
            # Show all stored bullets below
                # Hovering over any bullet in this menu shows its stats
            # Show red circle buttons around each Chamber "slot", except the "slot" in 1st position
                # Allow player to rotate Chamber

            # Options:
                # Player left-clicks on stored bullet:
                    # Highlights stored bullet

                # Player left-clicks on a Chamber "slot"
                    # If a STORED bullet is highlighted:
                        # If clicked Chamber slot is empty:
                            # Add highlighted STORED bullet to chamber slot **
                        # If not empty:
                            # Remove highlight from STORED bullet
                    # If a STORED bullet is not highlighted:
                        # If a LOADED bullet is in clicked Chamber slot:
                            # Highlight LOADED bullet

                    # If a LOADED bullet is highlighted:
                        # If clicked Chamber slot is empty:
                            # Move loaded bullet to clicked Chamber slot **
                        # If clicked Chamber slot is not empty:
                            # Swap positions of highlighted loaded bullet and bullet in clicked Chamber slot. **

                # Player right-clicks on a Chamber slot:
                    # If a loaded bullet is in Chamber slot, remove it. **
                
                # Player left-clicks Red Rotate Button:
                    # Rotate Chamber counter clockwise **
                        # Until (button that was clicked)'s slot is in 1st position
                    # Always confirm this action (even out of combat)
            
            # ** In combat, this uses 1 player turn
                # Always confirm these actions in combat


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    main()