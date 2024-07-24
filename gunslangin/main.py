import math
import pygame
import random
import sys
import stage as Stage
import slanger as Slanger
import bullet as Bullet

from bullet import EtherealBullet

# Constants:
FPS = 60
ROW = 3
COL = 9
TILE_SIZE = 100
SCREEN_WIDTH = (TILE_SIZE * 5) * 2
SCREEN_HEIGHT = (TILE_SIZE * 3) * 2
BUTTON_AREA_HEIGHT = 50

# Calculate the center of the screen
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

def display_bullet_info(screen, bullet, mouse_x, mouse_y):
    info_box_width = 150
    info_box_height = 70
    info_box_padding = 5

    # Calculate the position of the info box
    info_box_x = mouse_x + info_box_padding
    info_box_y = mouse_y + info_box_padding

    # Draw the background of the info box
    pygame.draw.rect(screen, BLACK, (info_box_x, info_box_y, info_box_width, info_box_height))
    pygame.draw.rect(screen, WHITE, (info_box_x, info_box_y, info_box_width, info_box_height), 2)

    # Display bullet information
    font = pygame.font.Font(None, 24)
    text_color = WHITE
    text_x = info_box_x + info_box_padding
    text_y = info_box_y + info_box_padding

    bullet_info = f"Health: {bullet.health}\nDamage: {bullet.damage}\nMovement: {bullet.movement_per_turn}"
    info_lines = bullet_info.split('\n')

    for line in info_lines:
        text = font.render(line, True, text_color)
        screen.blit(text, (text_x, text_y))
        text_y += text.get_height() + info_box_padding

def draw_loading_stage(slanger, highlighted_bullet_index=-1):
    # Clear the screen
    screen.fill(BLACK)

    # Calculate the center of the screen
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Constants for the gun cylinder
    cylinder_radius = 100
    bullet_size = 35
    bullet_padding = 10

    # Draw the gun cylinder
    pygame.draw.circle(screen, WHITE, (center_x, center_y), cylinder_radius, 3)

    # Draw six squares representing bullets in the gun cylinder
    for i in range(6):
        angle = (i / 6) * (2 * math.pi)  # Distribute the bullets evenly around the cylinder
        bullet_x = center_x + int(cylinder_radius * math.cos(angle)) - bullet_size // 2
        bullet_y = center_y + int(cylinder_radius * math.sin(angle)) - bullet_size // 2

        if i < len(slanger.loaded_bullets):
            bullet = slanger.loaded_bullets[i]
            if isinstance(bullet, EtherealBullet):
                pygame.draw.rect(screen, MAGENTA, (bullet_x, bullet_y, bullet_size, bullet_size))
            else:
                pygame.draw.rect(screen, YELLOW, (bullet_x, bullet_y, bullet_size, bullet_size))
            pygame.draw.rect(screen, WHITE, (bullet_x, bullet_y, bullet_size, bullet_size), 2)
        else:
            pygame.draw.rect(screen, BLACK, (bullet_x, bullet_y, bullet_size, bullet_size))
            pygame.draw.rect(screen, WHITE, (bullet_x, bullet_y, bullet_size, bullet_size), 2)

    # Calculate total width occupied by stored bullets
    total_stored_bullet_width = len(slanger.stored_bullets) * (bullet_size + bullet_padding)
    start_x_stored_bullets = (SCREEN_WIDTH - total_stored_bullet_width) // 2

    # Draw stored bullets along the bottom of the screen
    stored_bullet_size = 35
    stored_bullet_padding = 10

    for i, bullet in enumerate(slanger.stored_bullets):
        stored_bullet_x = start_x_stored_bullets + i * (stored_bullet_size + stored_bullet_padding)
        stored_bullet_y = SCREEN_HEIGHT - BUTTON_AREA_HEIGHT - stored_bullet_size - stored_bullet_padding
        if isinstance(bullet, EtherealBullet):
            color = MAGENTA
        else:
            color = YELLOW
        if i == highlighted_bullet_index:
            pygame.draw.rect(screen, BLUE, (stored_bullet_x, stored_bullet_y, stored_bullet_size, stored_bullet_size))
        else:
            pygame.draw.rect(screen, color, (stored_bullet_x, stored_bullet_y, stored_bullet_size, stored_bullet_size))
            pygame.draw.rect(screen, WHITE, (stored_bullet_x, stored_bullet_y, stored_bullet_size, stored_bullet_size), 2)
    
    # Draw arrow in the top-right corner pointing to the right
    arrow_size = 30
    arrow_padding = 10
    arrow_x = SCREEN_WIDTH - arrow_size - arrow_padding
    arrow_y = arrow_padding

    pygame.draw.polygon(screen, WHITE, [(arrow_x, arrow_y), (arrow_x + arrow_size, arrow_y + arrow_size // 2), (arrow_x, arrow_y + arrow_size)])

    # Update the display
    pygame.display.flip()
    CLOCK.tick(FPS)

def draw_stage(stage, player_slanger, cpu_slanger):
    # Clear the screen
    screen.fill(BLACK)

    stage_width = COL * TILE_SIZE
    stage_height = ROW * TILE_SIZE

    # Calculate the starting position to center the stage
    start_x = (SCREEN_WIDTH - stage_width) // 2
    start_y = (SCREEN_HEIGHT - stage_height) // 2

    # Draw menu
    menu_font = pygame.font.Font(None, 36)
    menu_player_turn_text = menu_font.render(f"Current Turn: {stage.current_turn.name}", True, WHITE)
    player_bullets_text = menu_font.render(f"Player Bullets: {len(player_slanger.loaded_bullets)}", True, WHITE)
    cpu_bullets_text = menu_font.render(f"CPU Bullets: {len(cpu_slanger.loaded_bullets)}", True, WHITE)
    player_movement_text = menu_font.render(f"Player Movement: {player_slanger.movement}", True, WHITE)
    cpu_movement_text = menu_font.render(f"CPU Movement: {cpu_slanger.movement}", True, WHITE)

    screen.blit(menu_player_turn_text, (SCREEN_WIDTH // 4, 10))
    screen.blit(player_bullets_text, (SCREEN_WIDTH // 4, 50))
    screen.blit(cpu_bullets_text, (3 * SCREEN_WIDTH // 4 - cpu_bullets_text.get_width(), 50))
    # Draw movement text based on the current turn
    if stage.current_turn == player_slanger:
        screen.blit(player_movement_text, (SCREEN_WIDTH // 4, 90))
    elif stage.current_turn == cpu_slanger:
        screen.blit(cpu_movement_text, (3 * SCREEN_WIDTH // 4 - cpu_movement_text.get_width(), 90))

    # Draw the "end turn" button
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - BUTTON_AREA_HEIGHT, SCREEN_WIDTH, BUTTON_AREA_HEIGHT))
    font = pygame.font.Font(None, 36)
    text = font.render("End Turn", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - BUTTON_AREA_HEIGHT // 2 - text.get_height() // 2))

    for row in range(ROW):
        for col in range(COL):
            tile_value = stage.stage_lanes[row][col]

            if player_slanger in tile_value:
                pygame.draw.rect(screen, GREEN, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if stage.option_selected == player_slanger:
                    # Add outline to tile
                    pygame.draw.rect(screen, BLUE, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                else:
                    pygame.draw.rect(screen, WHITE, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
            elif cpu_slanger in tile_value:
                pygame.draw.rect(screen, CYAN, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if stage.option_selected == cpu_slanger:
                    # Add outline to tile
                    pygame.draw.rect(screen, BLUE, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                else:
                    pygame.draw.rect(screen, WHITE, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
            elif isinstance(tile_value, list) and any(isinstance(item, Bullet.Bullet) for item in tile_value):
                if all(isinstance(item, Bullet.Bullet) for item in tile_value):
                    if len(tile_value) > 1:
                        bullet_list_rect = pygame.Rect(start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, YELLOW, bullet_list_rect)
                        pygame.draw.rect(screen, RED, bullet_list_rect, 1)
                    elif len(tile_value) == 1:
                        print(tile_value)
                        if isinstance(tile_value[0], EtherealBullet):
                            color = MAGENTA
                        else:
                            color = YELLOW
                        bullet_list_rect = pygame.Rect(start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, color, bullet_list_rect)
                        pygame.draw.rect(screen, WHITE, bullet_list_rect, 1)
            elif isinstance(tile_value, list) and not any(tile_value):
                pygame.draw.rect(screen, BROWN, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, WHITE, (start_x + col * TILE_SIZE, start_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)


def move_slanger(stage, slanger, direction=-1):
    if slanger == stage.player_left:
        slanger_row, slanger_col = stage.player_left_position
        stage.player_left_position = (slanger_row + direction, slanger_col)     # Set new coordinates
    elif slanger == stage.player_right:
        slanger_row, slanger_col = stage.player_right_position
        stage.player_right_position = (slanger_row + direction, slanger_col)     # Set new coordinates
    stage.stage_lanes[slanger_row][slanger_col] = []     # Update old position
    stage.stage_lanes[slanger_row + direction][slanger_col] = [slanger]    # Update lane with new position
    # Reset option selected and update slanger movement
    stage.option_selected = ""
    stage.current_turn.movement -= 1


def move_bullet(stage):
    for row in range(ROW):
        for col in range(COL):
            tile_value = stage.stage_lanes[row][col]
            if isinstance(tile_value, list) and any(isinstance(item, Bullet.Bullet) for item in tile_value):
                if all(isinstance(item, Bullet.Bullet) for item in tile_value):
                    for bullet in tile_value:
                        print("bullet instance")
                        bullet_row, bullet_col = bullet.coordinates

                        if bullet.direction == "left" and bullet.movement > 0 and stage.current_turn == stage.player_right:
                            print("moving player bullets...")
                            new_col = bullet_col - 1
                            if 0 <= new_col < COL:
                                handle_bullet_collision(stage, row, col, new_col, bullet)
                            else:
                                stage.stage_lanes[row][col] = []
                        elif bullet.direction == "right" and bullet.movement > 0 and stage.current_turn == stage.player_left:
                            print("moving CPU bullets...")
                            new_col = bullet_col + 1
                            if 0 <= new_col < COL:
                                handle_bullet_collision(stage, row, col, new_col, bullet)
                            else:
                                stage.stage_lanes[row][col] = []
                else:
                    stage.stage_lanes[row][col] = []
            if isinstance(tile_value, Bullet.Bullet):
                bullet = tile_value
                bullet_row, bullet_col = bullet.coordinates

                if bullet.direction == "left" and bullet.movement > 0 and stage.current_turn == stage.player_right:
                    new_col = bullet_col - 1
                    if 0 <= new_col < COL:
                        handle_bullet_collision(stage, row, col, new_col, bullet)
                    else:
                        stage.stage_lanes[row][col] = []
                elif bullet.direction == "right" and bullet.movement > 0 and stage.current_turn == stage.player_left:
                    new_col = bullet_col + 1
                    if 0 <= new_col < COL:
                        handle_bullet_collision(stage, row, col, new_col, bullet)
                    else:
                        stage.stage_lanes[row][col] = []


def handle_bullet_collision(stage, row, col, new_col, bullet):
    # Check the target tile for collision
    target_tile = stage.stage_lanes[row][new_col]

    if isinstance(target_tile, Slanger.Slanger):
        # Bullet collides with a slanger
        target_slanger = target_tile[0]
        target_slanger.health -= bullet.damage

        if target_slanger.health <= 0:
            stage.stage_lanes[row][new_col].remove(target_slanger)
            if target_slanger == stage.player_right:
                print("You win!")
            else:
                print("You lose!")

    elif isinstance(target_tile, list) and any(isinstance(item, Bullet.Bullet) for item in target_tile):
        # Bullet collides with another list of bullets
        for bullet_2 in target_tile:
            if not (isinstance(bullet, EtherealBullet) or isinstance(bullet_2, EtherealBullet)):
                if bullet.direction != bullet_2.direction:
                    bullet.health -= bullet_2.damage
                    bullet_2.health -= bullet.damage
                    if bullet_2.health <= 0:
                        stage.stage_lanes[row][new_col].remove(bullet_2)
        else:
            # Bullet survives, append it to the list
            stage.stage_lanes[row][new_col].append(bullet)
            # Remove bullets that have health <= 0
            stage.stage_lanes[row][new_col] = [b for b in stage.stage_lanes[row][new_col] if b.health > 0]
            stage.stage_lanes[row][col].remove(bullet)

    else:
        # No collision, move the bullet
        stage.stage_lanes[row][col].remove(bullet)
        stage.stage_lanes[row][new_col].append(bullet)
    bullet.coordinates = (row, new_col)
    bullet.movement -= 1


def main():
    print("Welcome gunslanger")
    print("Hi owen")

    # Init stage
    stage = Stage.Stage()
    stage.initialize_stage(ROW, COL)

    # Init slangers
    player_slanger = Slanger.Slanger(name="Player")
    cpu_slanger = Slanger.Slanger(name="CPU")
    player_round_movement = player_slanger.movement
    cpu_round_movement = cpu_slanger.movement

    # Init slanger coordinates
    stage.player_left = player_slanger
    stage.player_right = cpu_slanger
    stage.player_left_position = (1, 0)      # (y, x) / (row, col)
    stage.player_right_position = (1, COL-1) # (y, x) / (row, col)

    # Init turn
    stage.current_turn = player_slanger

    # Init stage lanes
    stage.stage_lanes[1][0] = [player_slanger]
    stage.stage_lanes[1][COL-1] = [cpu_slanger]

    # Init slanger bullets
    # player_slanger.loaded_bullets = [Bullet.Bullet() for _ in range(6)]
    player_slanger.stored_bullets = [EtherealBullet() for _ in range(3)] + [Bullet.Bullet() for _ in range(3)]
    # for bullet in player_slanger.stored_bullets:
    #     bullet.health = random.randint(50, 100)
    #     bullet.damage = random.randint(10, 20)
    #     bullet.movement_per_turn = random.randint(1, 5)
    #     bullet.movement = bullet.movement_per_turn
    cpu_slanger.loaded_bullets = [Bullet.Bullet() for _ in range(6)]
    cpu_slanger.stored_bullets = [Bullet.Bullet() for _ in range(6)]
    
    # Draw bullet loading screen
    draw_loading_stage(player_slanger)
    highlighted_bullet_index = -1
    bullet_info_box_displayed = False

    # Loading stage loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Quit Pygame
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x, mouse_y)

                # Check if the arrow was clicked
                arrow_size = 30
                arrow_padding = 10
                arrow_x = SCREEN_WIDTH - arrow_size - arrow_padding
                arrow_y = arrow_padding

                center_x = SCREEN_WIDTH // 2
                center_y = SCREEN_HEIGHT // 2
                cylinder_radius = 100

                if arrow_x <= mouse_x <= arrow_x + arrow_size and arrow_y <= mouse_y <= arrow_y + arrow_size:
                    running = False
                else:
                    # Check if a stored bullet was clicked
                    stored_bullet_size = 35
                    stored_bullet_padding = 10
                    start_x_stored_bullets = (SCREEN_WIDTH - len(player_slanger.stored_bullets) * (stored_bullet_size + stored_bullet_padding)) // 2
                    stored_bullet_y = SCREEN_HEIGHT - BUTTON_AREA_HEIGHT - stored_bullet_size - stored_bullet_padding

                    for i, bullet in enumerate(player_slanger.stored_bullets):
                        stored_bullet_x = start_x_stored_bullets + i * (stored_bullet_size + stored_bullet_padding)

                        if stored_bullet_x <= mouse_x <= stored_bullet_x + stored_bullet_size and stored_bullet_y <= mouse_y <= stored_bullet_y + stored_bullet_size:
                            # A stored bullet is clicked, set the highlighted index and redraw the loading stage
                            print(f"Highlighting bullet {bullet}")
                            highlighted_bullet_index = i
                            draw_loading_stage(player_slanger, highlighted_bullet_index)
                            break

                # Check if a cylinder square was clicked when a stored bullet is highlighted
                if highlighted_bullet_index != -1:
                    bullet_size = 35
                    bullet_padding = 10

                    for i in range(6):
                        angle = (i / 6) * (2 * math.pi)
                        bullet_x = center_x + int(cylinder_radius * math.cos(angle)) - bullet_size // 2
                        bullet_y = center_y + int(cylinder_radius * math.sin(angle)) - bullet_size // 2

                        if (
                            bullet_x <= mouse_x <= (bullet_x + bullet_size) and
                            bullet_y <= mouse_y <= (bullet_y + bullet_size)
                        ):
                            # Move the highlighted bullet from stored_bullets to loaded_bullets
                            print("appened bullet")
                            player_slanger.loaded_bullets.append(player_slanger.stored_bullets.pop(highlighted_bullet_index))
                            draw_loading_stage(player_slanger)  # Redraw the loading stage after the move
                            highlighted_bullet_index = -1
                            break
            elif event.type == pygame.MOUSEMOTION:
                # Get the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if a stored bullet was hovered
                stored_bullet_size = 35
                stored_bullet_padding = 10
                start_x_stored_bullets = (SCREEN_WIDTH - len(player_slanger.stored_bullets) * (stored_bullet_size + stored_bullet_padding)) // 2
                stored_bullet_y = SCREEN_HEIGHT - BUTTON_AREA_HEIGHT - stored_bullet_size - stored_bullet_padding

                for i, bullet in enumerate(player_slanger.stored_bullets):
                    stored_bullet_x = start_x_stored_bullets + i * (stored_bullet_size + stored_bullet_padding)

                    if stored_bullet_x <= mouse_x <= stored_bullet_x + stored_bullet_size and stored_bullet_y <= mouse_y <= stored_bullet_y + stored_bullet_size:
                        if not bullet_info_box_displayed:
                            screen.fill(BLACK)
                            draw_loading_stage(player_slanger, highlighted_bullet_index)
                            display_bullet_info(screen, bullet, mouse_x, mouse_y)
                            bullet_info_box_displayed = True
                    else:
                        bullet_info_box_displayed = False
        # Update the display
        pygame.display.flip()
        CLOCK.tick(FPS)

    # Draw fighting stage
    print(player_slanger.loaded_bullets)
    draw_stage(stage, player_slanger, cpu_slanger)

    # Fighting loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                start_x = (SCREEN_WIDTH - COL * TILE_SIZE) // 2
                start_y = (SCREEN_HEIGHT - ROW * TILE_SIZE) // 2
                grid_col = (mouse_x - start_x) // TILE_SIZE
                grid_row = (mouse_y - start_y) // TILE_SIZE

                # Check if the click is within the grid
                if 0 <= grid_col < COL and 0 <= grid_row < ROW:
                    # Check if slanger clicked...
                    slanger_row, slanger_col = stage.player_left_position if stage.current_turn == stage.player_left else stage.player_right_position

                    # Check the relation between the clicked tile and the player's slanger
                    if grid_row == slanger_row - 1 and grid_col == slanger_col:         # if above
                        # If slanger highlighted, check tile clicked for valid option
                        if stage.option_selected == stage.current_turn and stage.current_turn.movement > 0:
                            if (slanger_row, slanger_col) == stage.player_left_position:
                                move_slanger(stage, stage.player_left, direction=-1)
                            elif (slanger_row, slanger_col) == stage.player_right_position:
                                move_slanger(stage, stage.player_right, direction=-1)
                        else:
                            print(f"Invalid movement for {stage.current_turn.name}")
                        print("Moved slanger up...")
                    elif grid_row == slanger_row + 1 and grid_col == slanger_col:       # if below
                        # If slanger highlighted, check tile clicked for valid option
                        if stage.option_selected == stage.current_turn:
                            if stage.current_turn.movement > 0:
                                if (slanger_row, slanger_col) == stage.player_left_position:
                                    move_slanger(stage, stage.player_left, direction=1)
                                elif (slanger_row, slanger_col) == stage.player_right_position:
                                    move_slanger(stage, stage.player_right, direction=1)
                            else:
                                print(f"Not enough movement to move {stage.current_turn.name}")
                        print("Moved slanger down...")
                    elif grid_row == slanger_row and (grid_col == slanger_col + 1 or grid_col == slanger_col - 1):
                        # Placing a bullet...
                        bullet_shot = stage.current_turn.loaded_bullets.pop(0)
                        stage.stage_lanes[grid_row][grid_col].append(bullet_shot)
                        bullet_shot.coordinates = (grid_row, grid_col)
                        if stage.current_turn == player_slanger:
                            bullet_shot.direction = "right"
                        elif stage.current_turn == cpu_slanger:
                            bullet_shot.direction = "left"

                    elif grid_row == slanger_row and grid_col == slanger_col:
                        print("Slanger options")
                        if stage.current_turn == player_slanger:
                            if stage.option_selected is not player_slanger:
                                stage.option_selected = player_slanger
                            else:
                                stage.option_selected = ""                         
                        elif stage.current_turn == cpu_slanger:
                            if stage.option_selected is not cpu_slanger:
                                stage.option_selected = cpu_slanger
                            else:
                                stage.option_selected = ""
                    else:
                        print("No options")
                    
                    screen.fill(BLACK)
                    draw_stage(stage, player_slanger, cpu_slanger)

                elif SCREEN_HEIGHT - BUTTON_AREA_HEIGHT <= mouse_y <= SCREEN_HEIGHT:
                    # Update all bullet positions
                    move_bullet(stage)

                    # Reset movements and selections
                    stage.option_selected = ""
                    player_slanger.movement = player_round_movement
                    cpu_slanger.movement = cpu_round_movement

                    # Update all bullet movement values
                    for row in range(ROW):
                        for col in range(COL):
                            tile_value = stage.stage_lanes[row][col]
                            if isinstance(tile_value, list) and any(isinstance(item, Bullet.Bullet) for item in tile_value):
                                if all(isinstance(item, Bullet.Bullet) for item in tile_value):
                                    for bullet in tile_value:
                                        bullet.movement = bullet.movement_per_turn

                    # Switch stage.current_turn
                    stage.current_turn = cpu_slanger if stage.current_turn == player_slanger else player_slanger
                    print(f"Turn switched to {stage.current_turn.name}")

                    screen.fill(BLACK)
                    draw_stage(stage, player_slanger, cpu_slanger)
                    
        # Update the display
        pygame.display.flip()
        CLOCK.tick(FPS)

    # Draw town stage
    
    
    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gunslanger")
    main()