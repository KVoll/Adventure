Adventure
=========
This program is a project for a trainee position at a company using their API.  The goal of this project is to learn
and use the company's API while completing some essential tasks:
-- The player's stats, and the game environment should be read from XML.
-- The game should be able to be saved and reloaded.
-- The game needs to be a true text adventure with (verb, noun) commands.
-- Each person who plays should have a score.  (Not implemented yet)
-- Have a logging tool, and use git for version control

My game is incomplete and a work in progress.  The demos will be on Oct. 4, 2013.
As it stands, I have a working engine with minor formatting issues.
The current engine handles three main commands: look, open, and take.
The player can also open a menu (list of commands), save, and load.

The biggest thing my game lacks at this point is an engaging storyline.  The idea was to create a game heavy in story
with the main goal being to have to search and find items in order to find clues about how to escape a locked room with
hidden sub-rooms.  The scoring system (to be implemented) will be based on finding easter eggs in the game.  I wanted
to encourage the player to use every command on every object in the game.  The game handles obscure commands such as
"take room" in one of two ways, the player finds something hidden, or a witty response is displayed.  There is still
100 things I would like to add to the game, but the bulk of the work that needs to be implemented in the current
standing of this code is the storyline. 

KNOWN ISSUES:
- Story is a mixture of ideas, in first person, second person, past tense, present tense, and all sorts of confusing stuff.
  Fixing the story to be engaging, fun, and not confusing is HIGH PRIORITY.
- Incomplete XML
