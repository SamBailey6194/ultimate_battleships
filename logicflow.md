# WELCOMING USER
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 1 | Welcome User | Invite to log in or create user | ?? |
| 2 | User invited to log in or create user | Y = [Logging In](#user-logging-in), N = [User Creation](#user-creation) | ?? |

# USER LOGGING IN
## IF USER GOES TO LOGGING IN
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 3 | Logging In | Username asked for | ?? |
| 4 | Username Entered | Password asked for | ?? |
| 5 | Password Entered | Checks database for username and password | ?? |

## IF ONE MATCHES BUT OTHER DOESN'T OR NEITHER IS FOUND
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 6 | Error Message | Tell user the login is invalid and asks for then to try again | ?? |

[See User Goes To Logging In](#if-user-goes-to-logging-in)

This step for security reasons doesn't provide which wasn't a match.
This then means the user has to remember both parts of information.

## IF USERNAME AND PASSWORD MATCHES
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 6 | Username and Password Matched | Welcomes User back | ?? |
| 7 | Checks for saved games database | If username found, asks user if they want to [load any games](#if-saved-games-finds-username), if username not found = starts a [new game](#gameplay-logic) | ?? |

## IF SAVED GAMES FINDS USERNAME
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 8 | User enters Y or N | Y = List of games saved displayed, N = New game starts, Any other input repeats asking user for Y or N to be inputted | ?? |

For N = New Game, go to [gameplay flow chart](#gameplay-logic)

## IF USER REQUESTS TO LOAD A SAVED GAME
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 9 | Asks user for game they want to reload | User enters the number associated with game they want to load | ?? |
| 10 | User input validation | If input entered is a number next to a game = [loads the associated game](#loaded-game), If input is not a number next to a game or not a number = error message and repeats asking for number associated with a game listed | ?? |

## LOADED GAME
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 11 | Game ID Fetched | Game loads and the program retrieves the Game ID to help with saving later | ?? |
| 12 | Game Boards Converted and Stylised | Game boards in the save file are converted back to a grid and the colours are added back in, then displayed | ?? |
| 13 | Game continues | Game then continues, see [gameplay flow chart](#gameplay-logic) | ?? |

# USER CREATION
## IF USER GOES TO USER CREATION
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 3 | Asks user to create a username | Checks username meets requirements | ?? |

## IF USERNAME MEETS REQUIREMENTS
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 4 | Username meets requirements | Adds username to database and asks user to create a password | ?? |
| 5 | Asks user to create a password | Checks password meets requirements | ?? |

## IF PASSWORD MEETS REQUIREMENTS
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 4 | Password meets requirements | Adds password to database and links it to username, then starts a [new game](#gameplay-logic) | ?? |

# GAMEPLAY LOGIC
The steps in this are multinumbered because if you come from different points in the logic flow you will be at a different number. See the key below:

| Accessed Game from | Last Step Number | Step Number Gameplay continues from |
| ----- | ----- | ----- |
| New user just created a username and password | 4 | 5 |
| Username not found in database | 7 | 8 |
| User doesn't want to load from a saved game | 8 | 9 |
| User loads a saved game state | 13 | 14 |

Therefore the step in the below table will look like 5 / 8 / 9 to associate with where the gameplay logic was accessed from. The 14 will be added to the list once we get to taking turns, as the loaded game won't need the user choices of what size board and ship placement

## NEW GAME STARTS
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 5 / 8 / 9 | New game starts | Asks user for the board size they want to play on | ?? |
| 6 / 9 / 10 | User selection validation | 1 = 5x5 Grid created and displayed, 2 = 10x10 Grid created and displayed, 3 = 15x15 Grid created and displayed, any other input will ask user to input correct number | ?? |
| 7 / 10 / 11 | User Places Ships | From the user selection determines how many ships are available, the user enters the row first only when input is valid will it then ask for column. Once column is valid it will display the new board with the ship placed. | ?? |

Valid ship placement is from 0 to board size -1, and has to be a location that the user hasn't placed at yet when combining row and column. If user has already placed it will ask user to do row and column both again

| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 8 / 11 / 12 | All ships placed | Once user has placed all ships their board is shown and the computer's ships are placed randomly, then both boards are displayed, users board shows ship placement and computers board doesn't show ships. | ?? |

## TURNS
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 9 / 12 / 13 / 14 | Players Turn | User is now asked to shoot at row first, if valid input the column is asked for, if valid input user gets feedback on their shot | ?? |

Valid coordinate are from 0 to board size -1, and where they haven't shot yet

| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 10 / 13 / 14 / 15 | If valid coordinates user receives shot feedback | User is told if they Hit or Missed and how many ships are left to destroy | ?? |
| 11 / 14 / 15 / 16 | Computer random shot | Computer generates a random shot and gets feedback if they Hit or Missed and how many ships are left to destroy | ?? |
| 12 / 15 / 16 / 17 | Updated boards and scores displayed | User board is shown with computer shots, computer's board is shown with user shots, and both user and computer scores are shown | ?? |
| 13 / 16 / 17 / 18 | Game over check | If both user and computer have destroyed the other players ships = game ends in a tie. If user has destroyed computer's ships = User declared winner. If computer has destroyed user's ships = Computer declared winner. If ships remain for both user and computer = [game continues](#game-continues) | ?? |

If game is a tie or a winner declared then go to [game over](#game-over)

## GAME OVER
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 14 / 17 / 18 / 19 | Game is over | Scores are added to leaderboard and user is shown the updated leaderboard to see where they are | ?? |

Go to [exit game](#exit-game)

## GAME CONTINUES
| Step | Action | Outcome | Pass / Fail |
| ----- | ----- | ----- | ----- |
| 14 / 17 / 18 / 19 | Used asked to select an option between continuing, saving or exiting | C = game continues and [turns](#turns) is repeated, S = game state is saved to Google Sheets and game is exited, E = game is exited, any other input the user is asked to put in a correct input | ?? |

If game is exited, go to [exit game](#exit-game)

## EXIT GAME
| 15 / 18 / 19 / 20 | Game is exited | To double check user wanted to exit the program or the game, user is asked if they want to play again or exit program | ?? |
| 16 / 19 / 20 / 21 | User input validation | P = play again and user is asked about loading a saved game or not; see expected logic [here](#loaded-game); E = Program is exited  | ?? |
| 17 / 20 / 21 / 22 | Program exited | Program is completely exited  | ?? |