import os
from time import sleep
import ascii_art
from game import Game
from Q2API.util import logging
import traceback

logger = logging.out_file_instance("game_log")


def main():
    if os.listdir("saved_files"):
        file_name = prompt_save()
        game = Game(file_name)

    else:
        game = Game("creepy.xml")
        print game.state.something[0].value

        # Slow text via sleep for intro
        # for char in game.intro[0].value:
        #     sys.stdout.write(char),
        #     sleep(0.025)
        # sys.stdout.write('\n')
        # sleep(1.5)

    # ASCII intro picture
    # ascii_img = ascii_art.get_ascii_image()
    # ascii_img.get_image("title.png")

    print game.state.tip[0].value

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
        if len(words) == 1 and words[0] != "l" and words[0] not in game.keywords:
            verb = words[0]
        else:
            verb = words[0]
            verb = game.verbs.get(verb, "")
            # Join the remaining words as the noun.
        noun = ' '.join(words[1:])

        return verb, noun
    except IndexError:
        print "<Sorry, unable to process input.  Please try again.>\n"


def prompt_save():
    saved_game = os.listdir("saved_files")
    if saved_game:
        for i, fin in enumerate(saved_game):
            print str(i) + "\t" + fin.split(".")[0]
        choice = raw_input("Choose a saved game or type 'N' for a new game.\n> ")

        if choice.lower() not in ["n", "new"]:
            try:
                file_name = "saved_files/" + saved_game[int(choice)]
            except IndexError:
                print "Invalid choice.  Starting new game..."
                file_name = "creepy.xml"
        else:
            file_name = "creepy.xml"
    else:
        file_name = "creepy.xml"

    return file_name


if __name__ == "__main__":
    try:
        main()
    except:
        exception_string = traceback.format_exc()
        logger.write_line([exception_string])
        print exception_string