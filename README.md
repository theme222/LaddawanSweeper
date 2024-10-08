# LaddawanSweeper
## About
This project was created as a final project of the class "โปรแกรมภาษาคอมพิวเตอร์"
## How to setup
Install all dependancies and run the main.py with your specific discord TOKEN in the token.env file.
## Current commands {Prefix : "$"}
- **$start {difficulty}**
  - Start a game of Laddawan Sweeper™.
  - difficulty : easy (5x5), medium(7x7), hard(10x10), impossible(12x12)
  - These games are unique to their specific channel in which you run the command from.
- **$select {x} {y}**
  - Select a position to check.
  - x : The x position (column)
  - y : The y position (row)
  - You can also type two numbers with a space in the same channel to run this command as well
- **$flag {x} {y}**
  - Select a position to flag.
  - x : The x position (column)
  - y : The y position (row)
- **$surrender**
  - Surrender the game
- **$view**
  - View the current board
- **$help**
  - Help menu
