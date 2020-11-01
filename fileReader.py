import csv


"""
|--------------------------------------|
|======================================|
| THIS FILE CONTAINS ALL THE FUNCTIONS |
|   THAT READ FROM TEXT AND CSV FILES  |
|    \ CREDENTIALS/PROXIES/MESSAGES/   |
|======================================|
|--------------------------------------|
"""


 # Reads from proxy list and returns a proxy list :0
def readFromProxies(proxy_filename = 'proxy_list.txt'):

     # Proxies list to be returned
    proxies = []

    try:
        # Open the proxies file
        proxies_file = open(proxy_filename)

        # Pass data into proxies list
        for line in proxies_file:
            data_line = line.rstrip()    
            if data_line:             
                prx = data_line  # proxy ip
                proxies.append(prx.strip())
        # Close file
        proxies_file.close()
    except IOError:
        print ("Unable to read proxies from : %s!\nExit!" % proxy_filename)
        exit(0)
    return proxies

 # Reads from Messages list and returns a list 
def readFromMessages(message_filenane = 'messages_list.txt'):

     # Message list to be returned
    messages = []

    try:
        # Open the messages file
        messages_file = open(message_filenane)

        # Pass data into messages list
        for line in messages_file:
            data_line = line.rstrip()    
            if data_line:
                msg = data_line  # message x
                messages.append(msg.strip())

        # Close file
        messages_file.close()
    except IOError:
        print('Unable to read messages from :%s!\nExit!' % message_filenane)
        exit(0)

    return messages



 # Reads from credentials csv and fills usernames and passwords with data
def readCredentials(usrnm,psswd,credentials_filename = 'credentials.csv'):

    try:
        # Open the csv file
        csv_file = open(credentials_filename)
        # Pass data into usrnm , psswd lists
        for idx,line in enumerate(csv_file):
            data_line = line.rstrip()
            if data_line:
                data_line = data_line.rstrip().split(',') # Split line fields
                try:
                    usr = data_line[0]  # Username
                    pas = data_line[1]  # Password

                    usrnm.append(usr.strip())
                    psswd.append(pas.strip())
                except:
                    print ('Check your credentials file!Line %i'%idx)

        # Close file
        csv_file.close()
    except IOError:
        print('Unable to read credentials from : %s!\nExit!' %credentials_filename)
        exit(0)
