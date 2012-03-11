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
canal = "#hmm-la-bd"
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
        self.botDico = pylearndico.PylearnDico()

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
        if ((len(admins) == 0) or (author in admins)):
            # Command detection
            if (msg_list[0] == "!die"):
                ircbot.SingleServerIRCBot.die(self, quitmsg)
            if (msg_list[0] == "!off"):
                self.activated = False
                serv.privmsg(canal, "Ok, I won't say anything.")
            if (msg_list[0] == "!on"):
                self.activated = True
                serv.privmsg(canal, "Here we go!")
            if (msg_list[0] == "!save"):
                self.botDico.saveDico("dico.save")
                serv.privmsg(canal, "Done saving.")
            if (msg_list[0] == "!load"):
                self.botDico.loadDico("dico.save")
                serv.privmsg(canal, "Done loading.")
            if (msg_list[0] == "!search"):
                if (len(msg_list) > 1):
                    serv.privmsg(canal, self.botDico.getSentenceWithName(msg_list[1]))
                else:
                    serv.privmsg(canal, "Please provide at least a word.")
            if (msg_list[0] == "!ratio"):
                if (len(msg_list) == 1):
                    serv.privmsg(canal, "I will answer to 1/" + str(self.ratio) + " of the messages.")
                else:
                    try:
                        neoRatio = int(msg_list[1])
                        if ((neoRatio < 1) or (neoRatio > 100)):
                            serv.privmsg(canal, "The value must be between 1 and 100.")
                        else:
                            self.ratio = neoRatio
                            serv.privmsg(canal, "New ratio : I will answer to 1/" + str(self.ratio) + " of the messages")
                    except (ValueError, IndexError):
                        serv.privmsg(canal, "Incorrect parameter.")
            if (msg_list[0] == "!say"):
                serv.privmsg(canal, self.botDico.getSentence())
            if (msg_list[0] == "!stats"):
                serv.privmsg(canal, "I know " + str(self.botDico.getStats()) + " words!")
        # No command
        if (message[0] != "!"):
            #print(author + " : " + message)
            self.botDico.parse(message)
            if (self.activated):
                if (random.randint(0, self.ratio) == 0):
                    serv.privmsg(canal, self.botDico.getSentence())

# Starting bot
PylearnBot().start()
