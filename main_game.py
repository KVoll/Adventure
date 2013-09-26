import os
from Q2API.util import logging
import traceback
from game import Game
from time import sleep
import sys


logger = logging.out_file_instance("game_log")

def main():
    if os.listdir("Saved_Files"):
        file_name = prompt_save()
        game = Game(file_name)

    else:
        game = Game("Q2API_XML/creepy.xml")
        # print game.state.something[0].value
    os.system('cls')
        # Slow text via sleep for intro
    # for line in game.intro.split("        "):
    #     sys.stdout.write(line),
    #     sleep(1.0)
    # # sys.stdout.write(game.intro)
    # sleep(3)

    # ASCII intro picture
    # ascii_img = ascii_art.get_ascii_image()
    # ascii_img.get_image("title.png")
    print game.state.intro[0].value
    print game.state.tip[0].value

    print game.room.attrs["name"].upper()
    print game.room.desc[0].value

    quit_game = False
    while not quit_game:
        command = run_command(game)
        quit_game = game.update(command)


def run_command(game):
    command = raw_input("> ")
    if command == '':
        print "<Oops! Something went wrong.  Try again.>\n"
    else:
        if command.lower().strip() in game.keywords:
            key_func = game.key_words[command.lower().strip()]
            key_func(game)
        # Otherwise, attempts to find the verb, noun command to proccess.
        # Returns the result of the action's function.
        else:
            try:
                verb, noun = parse(command, game)
                func = game.actions[verb]
                res = func(game, noun)
                if res is not None:
                    print res
            except KeyError:
                # Excepts KeyErrors in the case of an invalid command.
                print "Invalid command.\n"


def parse(command, game):
    """ Parses the input and tries to find a verb, noun combo to return."""
    words = command.lower().strip().split()
    try:
    # If the command is only one word, set it as verb
        if len(words) == 1:
            verb = game.verbs[words[0]]
            noun = ""
        else:
            verb = game.verbs[words[0]]
            # Join the remaining words as the noun.
            noun = ' '.join(words[1:])

        game.list_used.append(command)
        game.nouns.append(noun)
        return verb, noun
    except IndexError:
        print "<Sorry, unable to process input.  Please try again.>\n"


def prompt_save():
    saved_game = os.listdir("Saved_Files")
    choice = raw_input("Welcome to In.  Would you like to start a saved game? (y/n)\n> ")
    if choice == 'y':
        if saved_game:
            for i, fin in enumerate(saved_game):
                print str(i) + "\t" + fin.split(".")[0]
            choice = raw_input("Choose a saved game or type 'N' for a new game.\n> ")
        try:
                file_name = "Saved_Files/" + saved_game[int(choice)]
        except IndexError:
            print "Invalid choice.  Starting new game..."
            file_name = "Q2API_XML/creepy.xml"
    else:
        file_name = "Q2API_XML/creepy.xml"

    return file_name


if __name__ == "__main__":
    try:
        main()
    except:
        exception_string = traceback.format_exc()
        logger.write_line([exception_string])
        print exception_string