# python C:\Python27\Lib\Q2API\xml\mk_class.py C:\Users\KVOll\PycharmProjects\Adventure\Q2API_XML\creepy.xml
# cd C:\Users\KVOll\PycharmProjects\Adventure python main_game.py
import os
import sys
from Imports.Stack import stack
from Q2API_XML import creepy
from colorconsole import terminal
from time import sleep
from Imports import ascii_art
import pygame.mixer

class Game():
    verbs = {'look': 'l', 'scan': 'l', 'view': 'l', 'scout': 'l', 'explore': 'l', 'l': 'l',
             'inspect': 'l', 'check': 'l', 'search': 'l', 'examine': 'l', 'read': 'l',
             'take': 't', 'get': 't', 'obtain': 't', 'steal': 't', 'remove': 't', 't': 't',
             'open': 'o', 'access': 'o', 'use': 'o', 'o': 'o', 'enter': 'e'}
    keywords = ['exit', 'inv', 'menu', 'save', 'score', 'memories']   # , 'list', 'nouns'
    screen = terminal.get_terminal()

    def __init__(self, file_name, sound):
        """ Initialize the game objects """
        # Get the XML data from file given
        with open(file_name, "r") as fin:
            xml_file = fin.read()
        self.nouns = []
        self.list_used = []
        self.sound = sound
        self.success, self.state = creepy.obj_wrapper(xml_file)     # Get the game state from Q2API obj_wrapper
        self.player_inv = self.state.player[0].inventory[0]         # Creates an instance of the inventory_q2class
        self.intro = self.state.intro[0].value
        self.room = self.get_current_room()
        self.exit_links = self.get_areas()
        self.player_room = self.state.player[0].room
        self.memories = self.state.player[0].memories[0].attrs["memory"].split(".")
        self.score = int(self.state.player[0].score[0].attrs["val"])
        self.computer_used = self.state.player[0].computer[0].attrs["used"]

    def display_score(self, num=0):
        if num != 0:
            print " "*num + "  Your current score is:  " + str(self.score)
        else:
            print "Your current score is:  " + str(self.score)

    def get_current_room(self):
        for room in self.state.room:
            if room.attrs["name"] == self.state.player[0].room[0].attrs["name"]:
                self.nouns.append(room.attrs["name"])
                return room

    def get_areas(self):
        temp_dict = {}
        for area in self.state.room:
            for exits in area.exit:
                exit_to = exits.attrs["to"]
                for room in self.state.room:
                    if room.attrs["name"] == exit_to:
                        temp_dict.setdefault(exits.attrs["link"], room)
        return temp_dict

    def check_score(self, item, num):
        print(item.score[0].prompt[0].value)
        self.score += int(item.score[0].attrs["point"])
        self.display_score(num)
        pygame.mixer.init()
        sound = pygame.mixer.Sound("Sounds/nintendo_08.wav")
        sound.set_volume(.10)
        sound.play()
        # print("Current score is:    " + str(self.score))
        print(" "*num + "  Memory added: " + item.score[0].memory[0].value + "\n")

        self.memories.append(item.score[0].memory[0].value)
        self.state.player[0].memories[0].attrs["memory"] += item.score[0].memory[0].value
        self.state.player[0].score[0].attrs["val"] = str(self.score)
        for score in item.score:
            item.score[0].attrs["point"] = "0"
            item.children.remove(score)

    def cmd_look(self, noun, place=None):
        """ cmd_look is a recursive function that processes a 'look' command for the player """
        # global verbs
        #ascii = ascii_art.get_ascii_image()
        #print(self.scores_available)
        text = ""
        num = len("[LOOK AT " + noun.upper() + "]>  ")

        # If place is none the intended place is the current room
        if place is None:
            place = self.room

        # If noun is not given the intended noun is the current room
        if noun == "":
            text = " <You see a "
            print "[LOOK AROUND ROOM]>  ",
            num = len("[LOOK AROUND ROOM]>  ")
            print place.l[0].value
            # For all items in the current place
            for item in place.item:
                # If item is visible in the same place, generate appropriate text
                if item.visible[0].attrs["in"] == place.attrs["name"]:
                    text += item.attrs["type"]
                    text += ", a "
            text = " "*num + text[:-4] + ".>\n"
            # Return the generated text to be printed
            return text
        # Otherwise, the noun is given
        else:
            temp_list = []
            # For each item in the noun given
            for item in place.item:
                # If the item's type is the same as the noun
                if item.attrs["type"] == noun:
                    print "[LOOK AT " + noun.upper() + "]>  ",
                    # Print appropriate response from XML
                    print item.l[0].value
                    # For each child object in the item
                    for child in item.item:
                        # If the item type is the same as where the child is visible, and the child has no requirements
                        if item.attrs["type"] == child.visible[0].attrs["in"] and len(child.requirement) == 0:
                            # If a list of children exists
                            if len(item.item) > 0:
                                # Append to temporary list
                                temp_list.append(child.attrs["type"])
                    # Check if item triggers a memory on look
                    if item.score and item.score[0].attrs["point"] != "0" and \
                            item.score[0].attrs["on"].split()[0] == "l":
                                self.check_score(item, num)

                    temp_str = ""
                    # If temporary list isn't empty
                    if temp_list:
                        # Return the words in the list as a string for output
                        for i in range(len(temp_list)):
                            temp_str += temp_list[i]
                            temp_str += ", a "
                        return " "*num + "  <You see a " + temp_str[:-4] + ".>\n"

                # Otherwise, make a recursive call back to find the given noun/item
                else:
                    text = self.cmd_look(noun, item)

            # Returns string obtained from list
            return text

    def cmd_open(self, noun, place=None):
        """ cmd_open is a recursive function that processes a 'open' command from the player. """
        temp_list = []
        num = len("[OPEN " + noun.upper() + "]> ")

        # Get list of inventory items
        if self.player_inv.attrs["items"] != "":
            player_inv = self.player_inv.attrs["items"].split(", a ")
            # Remove any empty strings from player_inventory
            for i in range(len(player_inv)):
                if player_inv[i] == "":
                    player_inv.pop()
        else:
            player_inv = []

        # If place is None, the intended place is the current room object
        if place is None:
            place = self.room

        # If a noun wasn't given, the intended place is the current room. Prints appropriate text.
        if noun == "":
            print "[OPEN ROOM]> ",
            return place.o[0].value
        # Otherwise, if the noun is non-empty
        elif noun != "":
            # Search for item in the place given
            for item in place.item:
                # If the item is the same as the noun, the item is found
                if item.attrs["type"] == noun:

                    if item.special:
                        return self.special_item(item)

                    print "[OPEN " + noun.upper() + "]> ",
                    if item.requirement:
                        req = item.requirement[0].attrs["req"]
                        # if ", " in req:
                        #     self.special_case(req, item, temp_list)

                        if str(req).startswith("o "):
                            if place.attrs["inspected"] != "1":
                                print item.requirement[0].prereq[0].value

                            else:
                                self.requirement_met(item, temp_list)
                                if item.attrs["type"] in self.exit_links.keys():
                                    self.room_change(item)
                        elif req not in player_inv:
                            print item.requirement[0].prereq[0].value
                        else:
                            self.requirement_met(item, temp_list)
                            if item.attrs["type"] in self.exit_links.keys():
                                self.room_change(item)
                    else:
                        self.requirement_met(item, temp_list)
                        if item.attrs["type"] in self.exit_links.keys():
                            self.room_change(item)

                    # Print the appropriate temporary text
                    temp_str = ""
                    if temp_list:
                        for i in range(len(temp_list)):
                            temp_str += temp_list[i]
                            temp_str += ", a "
                        return " " * num + "  <You see a " + temp_str[:-4] + ".>\n"
                    else:
                        return "\n"

                # Otherwise, if the item is not the noun given, make recursive call until item is found
                else:
                    res = self.cmd_open(noun, item)
                    if res is not None:
                        print res
            # Returns None to the caller
            return

    def special_item(self, item):
        if self.player_inv.attrs["items"] != "":
            player_inv = self.player_inv.attrs["items"].split(", a ")
            # Remove any empty strings from player_inventory
            for i in range(len(player_inv)):
                if player_inv[i] == "":
                    player_inv.pop()
        else:
            player_inv = []

        if item.attrs["type"] == "computer":
            self.computer(player_inv)
            print "Shutting down..."
            sleep(3)
            #self.sound.set_volume(.10)
            #self.sound.play()
            self.screen.clear()
            print
        elif item.attrs["type"] == "metal door":
            self.metal_door(player_inv, item)

    def computer(self, player_inv):
        keyword = "salt"
        password = "031415purple"

        self.screen.clear()

        #self.sound.fadeout(500)
        #sleep(.5)
        pygame.mixer.init()
        sound = pygame.mixer.Sound("Sounds/iMac_Startup.wav")
        sound.set_volume(.10)
        sound.play()

        ascii_img = ascii_art.get_ascii_image()
        ascii_img.get_image("computer.png")

        print "You can type quit, leave, or stop to stop trying the password.\nThe only thing you can access while" \
              " using the computer is your memories.\n"

        while 1:
            enter_pass = raw_input("Enter password:    ")
            if enter_pass == "quit" or enter_pass == "leave" or enter_pass == "stop":
                #print "Shutting down computer."
                break
            elif enter_pass == "memories":
                self.display_memories()
            elif enter_pass != password:
                print "Password incorrect.\n" \
                      "[Hint:  Irrational Date (mmddyy) + Favorite Color. No spaces or capitals.]\n "
            elif enter_pass == password:
                # self.machine_used = True
                enter_keyword = raw_input("Enter the keyword:    ")
                if enter_keyword.lower() != keyword:
                    print "Sorry, keyword incorrect.  Cannot decrypt message.  Shutting down for security " \
                          "measures.  Try again later when you know the correct keyword.\n"
                    # break
                else:
                    if "journal" not in player_inv:
                        print "The encryption is not detected in your inventory." \
                              "\nTry again later when you have the encryption.\n"
                        # break
                    elif "journal" in player_inv:
                        print "Detected encryption..."
                        sleep(1)
                        # Case 1 = Both False (0, 0) -> Fail
                        if "decryption table" not in player_inv and "recipe" not in player_inv:
                            print "Sorry, you do not have the decryption table or recipe needed to translate " \
                                  "message.  Try again later when you have the decryption table and recipe.\n"
                            # break
                        # Case 2 = One False, One True (0, 1) -> Fail
                        elif "decryption table" not in player_inv and "recipe" in player_inv:
                            print "Sorry, you do not have the decryption table needed to translate message.  " \
                                  "Try again later when you have the decryption table.\n"
                            # break
                        # Case 3 = One False, One True (1, 0) -> Fail
                        elif "decryption table" in player_inv and "recipe" not in player_inv:
                            print "Sorry, you do not have the recipe needed to translate message.  Try again " \
                                  "later when you have the recipe.\n"
                            # break
                        # Case 4 = Both True (1, 1) -> Win
                        elif "decryption table" in player_inv and "recipe" in player_inv:
                            self.computer_used = "True"
                            self.state.player[0].computer[0].attrs["used"] = "True"
                            print "Detected decryption table..."
                            sleep(1)
                            print "Detected recipe..."
                            sleep(1)
                            print "Decrypting message..."
                            sleep(1)
                            print "Decryption successful.\nLatch no. 1 has been released.\nYou hear a loud noise " \
                                  "coming from the other room.\n\nTHE MACHINE UNLOCKED A LATCH ON THE METAL DOOR.\n"
        # cont = raw_input("Press [ENTER] to continue.")

    # def cont(self):
    #     cont = raw_input("Press [ENTER] to continue.")
    #     while 1:
    #         if cont == "":
    #             return

    def metal_door(self, player_inv, item):
        if self.computer_used == "False" and "badge" not in player_inv:
            print "Must use computer to unlock latch no. 1 and badge to enter.\n"
        elif self.computer_used == "True" and "badge" not in player_inv:
            print "Must have badge to enter.\n"
        elif self.computer_used == "False" and "badge" in player_inv:
            print "Must use computer to unlock latch no. 1.\n"
        elif self.computer_used == "True" and "badge" in player_inv:
            pygame.mixer.init()
            pygame.mixer.fadeout(500)
            sound = pygame.mixer.Sound("Sounds/nintendo_15.wav")
            sound.set_volume(.10)
            sound.play()
            self.room_change(item)

    def room_change(self, item):
        #sound.set_volume(.10)
        self.room = self.exit_links[item.attrs["type"]]
        self.state.player[0].room[0].attrs["name"] = self.room.attrs["name"]

        if self.room.attrs["name"] != "living room":
            pygame.mixer.init()
            sound = pygame.mixer.Sound("Sounds/Galaga_ChallengeComp.wav")
            sound.set_volume(.10)
            sound.play()
            self.screen.cprint(3, 0, "")
            print "\n" + " "*50 + self.room.attrs["name"].upper()
            self.screen.cprint(15, 0, "")
            print self.room.desc[0].value
        else:
            self.screen.cprint(3, 0, "")
            print "\n" + " " * 50 + self.room.attrs["name"].upper()
            self.screen.cprint(15, 0, "")
            print self.room.desc[0].value
            #self.sound.mixer.fadeout(500)
            cont = raw_input("\n\nPress any key to continue.")
            if cont or cont == "":
                import main_game
                self.sound.fadeout(500)
                self.screen.clear()
                main_game.high_scores(self)
                again = raw_input("Play again? (y/n)\n")
                if again == "y":
                    main_game.main()
                else:
                    print("Closing game...")
                    sleep(1)
                    self.screen.clear()
                    sys.exit()


    def end_game(self):
        self.screen.cprint(3, 0, "")
        print "\n" + " " * 50 + self.room.attrs["name"].upper()
        self.screen.cprint(15, 0, "")
        print self.room.desc[0].value
        sleep(2)
        print("        You have completed the game and escaped the room. Thank you for playing!")
        sleep(1)
        print("        Your final score is: " + str(self.score) + "\n")
        sleep(1)
        print("Closing game...")
        sleep(2)
        self.sound.fadeout(500)
        #self.cmd_exit()

    def requirement_met(self, item, temp_list):
        print item.o[0].value
        for child in item.item:
            if child.visible[0].attrs["in"] == item.attrs["type"]:
                temp_list.append(child.attrs["type"])
        item.attrs["inspected"] = "1"

    def cmd_take(self, noun, place=None):
        """ cmd_take is a recursive function that processes a 'take' command from the player. """
        text = ""
        # Create stack for easier processing
        take_stack = stack()

        # Get list of inventory items
        if self.player_inv.attrs["items"] != "":
            player_inv = self.player_inv.attrs["items"].split(", a ")
            # Remove any empty strings from player_inventory
            for i in range(len(player_inv)):
                if player_inv[i] == "":
                    player_inv.pop()
        else:
            player_inv = []

        # If place is None, the intended place is the current room object
        if place is None:
            place = self.room

        # If no noun was given, the intended noun is the room
        if noun == "":
            print("[TAKE ROOM]>  "),
            text += place.t[0].value
            take_stack.push(text)
            if not take_stack.isEmpty():
                print str(take_stack.pop()) + "\n"

        # Else if the noun is non-empty
        elif noun != "":
            num = len("[TAKE " + noun.upper() + "]>  ")
            # Search for item in the place given
            for item in place.item:
                # If the item and noun are the same, the item is found
                if item.attrs["type"] == noun:
                    # print self.get_parent(item, place)
                    print("[TAKE " + noun.upper() + "]>  "),
                    # Check if the item is obtainable
                    if item.attrs["obtainable"] != "1":
                        # Check if item is already in inventory
                        if item.attrs["type"] in player_inv:
                            print(" "*num + "<The " + item.attrs["type"] + " is already in your inventory.>")
                        # Otherwise display text
                        else:
                            text = item.t[0].value
                            take_stack.push(text)
                            if not take_stack.isEmpty():
                                print str(take_stack.pop())
                    # Else if the parent object has not been inspected, print appropriate text
                    elif place.attrs["inspected"] != "1":
                        if item.requirement:
                            text += "    <You cannot take the " + item.attrs["type"] + " yet.>"
                            take_stack.push(text)
                            if not take_stack.isEmpty():
                                print str(take_stack.pop())
                        else:
                            self.take_item(item, take_stack, num)

                    # Otherwise, the item can be taken
                    else:
                        self.take_item(item, take_stack, num)

                # If the item in place is not the noun given, make recursive call until item is found
                else:
                    # Store and pass the parent's inspected status
                    self.cmd_take(noun, item)
            # When finished, returns empty string to make the caller happy, and to make printing statements easier
            return ""

    def take_item(self, item, take_stack, num):
        text = item.t[0].value
        text += "\n" + " " * num + " <Added " + item.attrs["type"] + " to inventory.>"
        # Append to inventory
        self.player_inv.attrs["items"] += item.attrs["type"] + ", a "
        # Change visibility status to inventory
        item.visible[0].attrs["in"] = "inventory"
        # Item is no longer obtainable
        item.attrs["obtainable"] = "0"
        take_stack.push(text)
        if not take_stack.isEmpty():
            print(str(take_stack.pop()))

    def cmd_menu(self):
        """ Shows a list of verb commands and their shortcuts, and key words that can be used. """
        commands = {}

        # Make reversed dict for printing.
        for (y, x) in self.verbs.items():
            commands.setdefault(x, []).append(y)

        shortcuts = commands.keys()
        verbs_list = commands.values()

        print "| SHORTCUTS |", "|   VERB COMMANDS"
        print "---------------------------------------------------------------------------------------------"

        # Print table for shortcuts and verb commands.
        for i in range(len(verbs_list)):
            count = 0
            print "|    ", shortcuts[i], "    | | ",
            words = sorted(verbs_list[i])
            for word in words:
                if count < len(words) - 1:
                    if word != shortcuts[i]:
                        print word + ",",
                else:
                    if word != shortcuts[i]:
                        print word
                count += 1

        print "---------------------------------------------------------------------------------------------"
        print "| KEY WORDS | | ",

        count = 0
        temp_str = ""

        # Print table for key words.
        for key_word in sorted(self.key_words.keys()):

            if count < len(self.key_words.keys()) - 1:
                if key_word == "inv":
                    temp_str += key_word + " (to show inventory), "
                else:
                    temp_str += key_word + ", "

        print temp_str[:-2]
        print "---------------------------------------------------------------------------------------------\n"

    def cmd_inv(self):
        """ Shows contents of inventory. """
        temp_str = ""
        if self.player_inv.attrs["items"] != "":
            player_inv = self.player_inv.attrs["items"].split(", a ")
            # Remove empty items
            for i in range(len(player_inv)):
                if player_inv[i] == "":
                    player_inv.pop()
        else:
            player_inv = []

        num = len(player_inv)

        if num == 0:                                                  # If inventory is empty
            print "[INVENTORY]>    Your inventory is empty.\n"    # Print corresponding text
        elif num == 1:                                                # Else if single item in inventory, print singular
            print "[INVENTORY]>    You have one item in your inventory: a " + \
                self.player_inv.attrs["items"][:-4] + ".\n"
        else:                                                         # Otherwise, print multiple items
            print "[INVENTORY]>    You have " + str(num) + " items in your inventory: a ",
            for i in range(len(player_inv)):
                temp_str += player_inv[i] + ", a "
            print temp_str[:-4] + ".\n"

    def cmd_exit(self):
        """ Safely close program. """
        import main_game
        affirm = raw_input("Do you want to exit? (y/n)\n")
        if affirm == "n":
            return
        elif affirm == "y":
            choice = raw_input("Would you like to save before exiting? (y/n)\n")
            if choice == "y":
                self.cmd_save()
                self.screen.clear()
                main_game.high_scores(self)
                again = raw_input("Play again? (y/n)\n")
                if again == "y":
                    main_game.main()
                else:
                    print("Closing game...")
                    sleep(1)
                    self.screen.clear()
                    sys.exit()
            else:
                self.screen.clear()
                main_game.high_scores(self)
                again = raw_input("Play again? (y/n)\n")
                if again == "y":
                    main_game.main()
                else:
                    print("Closing game...")
                    sleep(1)
                    self.screen.clear()
                    sys.exit()

    def cmd_save(self):
        """ Uses the Q2API to flatten the game state to new XML doc. """
        # Get file name for saving
        save_file = raw_input("Enter a name for saved game.\n>")

        # Flatten room object to XML
        saved_game_data = self.state.flatten_self()

        # Replace any spaces with an underscore
        if " " in save_file:
            save_file = save_file.replace(" ", "_")

        # Write saved data
        with open("Saved_Files\\" + save_file + ".xml", "w") as f:
            f.write(saved_game_data)

        file_list = os.listdir("Saved_Files")

        # If the file is in Saved_Files, print success. Otherwise, print error and try again
        if (save_file + ".xml") in file_list:
            print "Save successful.\n"

        # return room object
        return self.room

    def display_memories(self):
        num = len("[MEMORIES]>    ")
        print "[MEMORIES]>    ",
        if self.memories:
            print "You remember:"
            for memory in self.memories:
                print(" "*num + memory)
        else:
            print "You remember nothing.\n"

    # Action shortcuts mapped to respective function
    actions = {'l': cmd_look, 'o': cmd_open, 't': cmd_take}

    # Keywords mapped to their respective function
    key_words = {'exit': cmd_exit, 'menu': cmd_menu, 'inv': cmd_inv, 'save': cmd_save,
                 'score': display_score, 'memories': display_memories}# 'list': cmd_list, 'nouns': cmd_nouns,