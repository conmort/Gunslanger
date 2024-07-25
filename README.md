 # Overworld
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
        # Handle player movement:
            # Player enters combat tile:
                # Enter combat phase
            # Player enters non-combat tile:
                # Opens shop menu

    # Combat phase:
        # Quickdraw mini-game
            # Winner gets first move
        # First turn (Assume human player)
            # Player may move, shoot, load chamber, remove from chamber, "rotate" chamber
        # Second turn (Assume CPU player(s))
            # Player may move, shoot, load chamber, remove from chamber, "rotate" chamber
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
            # Show rewards menu
                # When exited, return to Overworld.

    # Button for "Chamber" menu (always visible)
        # When opened:
            # Show current Chamber in center
            # Show all stored bullets below
                # Hovering over any bullet in this menu shows its stats

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
            
            # ** In combat, this uses 1 player turn
