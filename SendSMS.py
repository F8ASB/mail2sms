#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Script to send SMS with number or List Number
#
#          F8ASB 2022 - F8ASB.COM
#

from imap_tools import MailBox, AND
import gammu
import sys, getopt
import phonelist as d
from datetime import datetime

# current date and time
now = datetime.now()
date = (now.strftime('%d-%m-%Y %H:%M'))

# Create object for talking with phone
state_machine = gammu.StateMachine()
# Read the configuration (~/.gammurc)
state_machine.ReadConfig()
# Connect to the phone
state_machine.Init()

# Send PIN if necessary
if state_machine.GetSecurityStatus() == 'PIN':
        state_machine.EnterSecurityCode('PIN', '1234')

def main(argv):

   user = ''
   number = ''
   liste = ''
   messages = ''

   try:
      opts, args = getopt.getopt(argv,"h:u:n:l:m:",["user=","phonenumber=","listnumber=","msg="])
   except getopt.GetoptError:
      print ('SendSMS.py -u <user> -n <phone number> -l <list phone number> -m <message>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('SendSMS.py -u <user> -n <phone number> -l <list phone number> -m <message>')
         sys.exit()
      elif opt in ("-u", "--user"):
         user = arg
      elif opt in ("-n", "--phonenumber"):
         number = arg
      elif opt in ("-l", "--listnumber"):
         liste = arg
      elif opt in ("-m", "--msg"):
         messages = arg

   if number != "":
       print ("number detected")
       envoiSMS(user,number,messages)
   if liste != "":
       print ("liste detected")
       envoiSMSMass(user,liste,messages)

def historiqueSMS(info):
    fichier = open("SMS.log", "a")
    fichier.write(info)
    fichier.close()
def envoiSMS(user,numero,message):

    if user in d.UserListe:

# Prepare message data
# We tell that we want to use first SMSC number stored in phone
        messageSMS = {
            "Text": message+" *-*NE PAS REPONDRE Serveur F8ASB *-*",
            "SMSC": {"Location": 1},
            "Number": numero,
        }

# Actually send the message
        state_machine.SendSMS(messageSMS)
        historiqueSMS(date+"/"+user+"/"+numero+">>"+message+"\n")
    else:
        print (user +">>> non autorisé")
        historiqueSMS(date+"/"+user+"/"+liste+">>"+message+"*!*NON AUTORISE\n")

def envoiSMSMass(user,liste,message):

# Transform dict to list
        for numero in d.Phonelist[liste].values():
            d.Numlist.append(numero)

        # Prepare SMS template
        messageSMS = {"Text": message+" *-*NE PAS REPONDRE Serveur F8ASB *-*", "SMSC": {"Location": 1}}

# Send SMS to all recipients on command line
        for number in d.Numlist:
            messageSMS["Number"] = number


            try:
                state_machine.SendSMS(messageSMS)
                historiqueSMS(date+"/"+user+"/"+liste+">>"+message+"\n")
            except gammu.GSMError as exc:
                print(f"Sending to {number} failed: {exc}")
                historiqueSMS(date+"/"+user+"/"+liste+">>"+message+"*!*ERREUR\n")

if __name__ == "__main__":
   main(sys.argv[1:])
