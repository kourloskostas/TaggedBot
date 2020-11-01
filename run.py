from fileReader import *
from someFunctions import *
import someFunctions
import os


"""
|------------------------------|
|    TAGGED.COM BOT PROJECT    |
|------------------------------|

"""
logging.info('Program Started')

# Lists of usernames/passwords/proxies and messages
usrnm = []  # Usernames
psswd = []  # Passwords
proxs = []  # Proxies
messg = []  # Messages

logging.info('Reading usernames/passwords...')
readCredentials(usrnm,psswd)

logging.info('Reading proxies...')
proxs = readFromProxies()

logging.info('Reading message options...')
messg = readFromMessages()

 # Number of bots to initiate
NUMBER_OF_BOTS = len(usrnm)-1

 # Sub proxy list , containing only working proxies
valid_proxies = validateProxies(proxs)


# Bot worker
def bot(id,PROXY):
    chrome_options = setDriverOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    dirpath = os.getcwd() # Path for current directory
    chrdriver_path = dirpath + '/chromedriver' # DIFFERENT ON UBUNTU >/ WINDOWS
    driver = webdriver.Chrome(executable_path=chrdriver_path,chrome_options=chrome_options)
    # Log user
    logUser(usrnm[id],psswd[id],driver)
    setFilters(driver)
    doStuff(driver) # After logging user in , start doing stuff


num_of_proxies = len(proxs)
 # Initialize a Thread for every bot
threads = [] # Thread list
for i in range(NUMBER_OF_BOTS): # Init Threads

    botproxy = proxs[i%num_of_proxies] # Proxy for bot
    t = threading.Thread(name = str(i) ,target=bot,args = (i,botproxy,))
    threads.append(t)
    t.start()


