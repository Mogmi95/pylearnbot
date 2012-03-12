#!/usr/bin/python2.7
#
# Project : Pylearnbot
# Author  : Mickael "Mogmi" Bidon
# Version : 1.1

# The learning structure
import pylearndico
# The IRC lib for Python
import irclib
# The IRC Bot lib for Python
import ircbot
# The random lib
import random

# The server you want the bot to connect to
server = "chat.freenode.org"
# Which port
port = 6667
# Channel where the bot will join
canal = "#lqdn-ccc"
# The name of the bot
name = "Mogbot"
# The description of the bot (/whois)
description = "http://mogmi.fr"
# The quit message
quitmsg = "Hmm..."
# List of users allowed to give orders. Let empty for everyone
admins = ["Mogmi"]

class PylearnBot(ircbot.SingleServerIRCBot):

    ## activate
    # Set if the bot answer on the channel or not
    ##
    activated = True

    ## ratio
    # The bot bot will answer to 1/ratio of the messages
    ##
    ratio = 10

    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(server, port)], name, description)
        self.botdico = pylearndico.PylearnDico()

    ## on_welcome(serv, ev)
    # Event starting when the bot connect to the server
    ##
    def on_welcome(self, serv, ev):
        serv.join(canal)

    ## on_pubmsg(serv, ev)
    # Event starting when a message is posted on the channel
    ##
    def on_pubmsg(self, serv, ev):
        author = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0]
        msg_list = message.split()
        admin_commands_list = {
                '!die' : lambda : self.bot_die(serv),
                '!off' : lambda : self.bot_off(serv),
                '!on' : lambda : self.bot_on(serv),
                '!save' : lambda : self.bot_save(serv),
                '!load' : lambda : self.bot_load(serv),
                '!search' : lambda : self.bot_search(serv, msg_list),
                '!setratio' : lambda : self.bot_setratio(serv, msg_list)
                }
        free_commands_list = {
                '!say' : lambda : self.bot_say(serv),
                '!stats' : lambda : self.bot_stats(serv)
                }
        if ((len(admins) == 0) or (author in admins)):
            try:
                admin_commands_list[msg_list[0]]()
            except (KeyError):
                pass
            try:
                free_commands_list[msg_list[0]]()
            except (KeyError):
                pass
        else:
            try:
                free_commands_list[msg_list[0]]()
            except (KeyError):
                pass

        # Auto answer
        if (message[0] != "!"):
            #print(author + " : " + message)
            self.botdico.parse(message)
            if (self.activated):
                if (random.randint(0, self.ratio) == 0):
                    serv.privmsg(canal, self.botdico.get_sentence())

    # Bot functions

    ## bot_die
    # Disconnect the bot from IRC
    ##
    def bot_die(self, serv, quitmsg):
        ircbot.SingleServerIRCBot.die(self, quitmsg)

    ## bot_off
    # Turn off bot auto-response
    ##
    def bot_off(self, serv):
        self.activated = False
        serv.privmsg(canal, "Ok, I won't say anything.")

    ## bot_on
    # Turn on bot auto-response
    ##
    def bot_on(self, serv):
        self.activated = True
        serv.privmsg(canal, "Let's talk!")

    ## bot_say
    # Make the bot say something
    ##
    def bot_say(self, serv):
        serv.privmsg(canal, self.botdico.get_sentence())

    ## bot_stats
    # Print how many words are known by the bot
    ##
    def bot_stats(self, serv):
        serv.privmsg(canal, "I know " + str(self.botdico.get_stats()) + " words!")

    ## bot_save
    # Save the current database
    ##
    def bot_save(self, serv):
        self.botdico.save_dico("dico.save")
        serv.privmsg(canal, "Done saving.")

    ## bot_load
    # Load the stored database
    ##
    def bot_load(self, serv):
        self.botdico.load_dico("dico.save")
        serv.privmsg(canal, "Done loading.")

    ## bot_search
    # Print a sentence which begin with a certain word
    ##
    def bot_search(self, serv, msg_list):
        if (len(msg_list) > 1):
            serv.privmsg(canal, self.botdico.get_sentence_with_name(msg_list[1]))
        else:
            serv.privmsg(canal, "Please provide at least a word.")

    ## bot_setratio
    # Change the ratio of the bot
    ##
    def bot_setratio(self, serv, msg_list):
        if (len(msg_list) == 1):
            serv.privmsg(canal, "I will answer to 1/" + str(self.ratio) + " of the messages.")
        else:
            try:
                neo_ratio = int(msg_list[1])
                if ((neo_ratio < 1) or (neo_ratio > 100)):
                    serv.privmsg(canal, "The value must be between 1 and 100.")
                else:
                    self.ratio = neo_ratio
                    serv.privmsg(canal, "New ratio : I will answer to 1/" + str(self.ratio) + " of the messages")
            except (ValueError, IndexError):
                serv.privmsg(canal, "Incorrect parameter.")

# Starting bot
PylearnBot().start()
