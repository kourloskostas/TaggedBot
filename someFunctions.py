import logging
import threading
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from botOptions import *

"""
|--------------------------------------|
|======================================|
| THIS FILE CONTAINS ALL THE ESSENTIAL |
|  FUNCTIONS ABOUT THE BOTS BEHAVIOUR  |
|-------\ LIKE/MESSAGE/REPLY /---------|
|======================================|
|--------------------------------------|
"""

# LOGGING OPTIONS
logging.basicConfig(stream = sys.stdout,filename = 'app.log', level = logging.INFO ,filemode = 'w' ,format=' %(asctime)s [%(levelname)s] (%(threadName)-9s) %(message)s',)
logging.getLogger().addHandler(logging.StreamHandler())
"""
    Check whether a proxy works or not
"""
def checkProxy(proxy,valid_proxies,lock):
    logging.info('Validating proxy : %s ...' , proxy)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    dirpath = os.getcwd() # Path for current directory
    chrdriver_path = dirpath + '/chromedriver'
    driver = webdriver.Chrome(executable_path=chrdriver_path,chrome_options=chrome_options)
    driver.set_page_load_timeout(BAD_PROXY_TIMEOUT)
    try:
        driver.get(homepage)
         # Switch to iframe in order for id elements to be visible
        try:
            frame = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login_frame')))
            driver.switch_to.frame(frame)
        except TimeoutException:
            logging.error('BAD PROXY : %s' , proxy)
            driver.quit()
            return False

    except:
        logging.warn('BAD PROXY : %s' , proxy)
        driver.quit()
        return False
    driver.quit()
    with lock:
        valid_proxies.append(proxy)
    return True

"""
    Validate proxy list
"""
def validateProxies(proxies):
    valid_proxies = [] # List of 
    lock = threading.Lock()
    proxy_threads = [] # Thread list
    
    for idx,proxy in enumerate(proxies): # Init Threads
        pvt_name  = ('Proxy Validator - ' + str(idx)) # Proxy validator thread
        t = threading.Thread(name = str(pvt_name) ,target=checkProxy,args = (proxy,valid_proxies,lock,))
        proxy_threads.append(t)
        t.start()

    for t in proxy_threads: # Init Threads
        t.join()

    # Validate proxies
    valid_proxy_number = len(valid_proxies) # Number of working proxies
    if (valid_proxy_number == 0):
        logging.error('No proxy is working!Exiting..')
        exit(0)
    elif(valid_proxy_number < 5):
        logging.warn('Only %s proxies working' ,valid_proxy_number)

    return valid_proxies






"""
    Set Driver Options
"""
def setDriverOptions():

    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    chrome_options.add_argument("--no-sandbox")
    """
    chrome_options.add_argument("--disable-impl-side-painting")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-seccomp-filter-sandbox")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-cast")
    chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
    chrome_options.add_argument("--disable-cloud-import")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-ipv6")
    chrome_options.add_argument("--allow-http-screen-capture")
    chrome_options.add_argument("--start-maximized")
    """
    chrome_options.add_argument("--incognito")
    # Disable on dev/debug 
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.

    return chrome_options

 # Visits url with driver
def visitUrl(driver , url):
    if (driver.current_url != url):
        try:
            driver.get((url))
        except:
            driver.quit()
            exit(1242)


 # Logs user on the site
def logUser(usernameStr ,passwordStr,driver):
     # Visit taggged
    visitUrl(driver,homepage)
    # Switch to iframe in order for id elements to be visible
    try:
        frame = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login_frame')))
        driver.switch_to.frame(frame)
    except TimeoutException:
        logging.error('Couldnt locate/switch to login frame!Check your proxy addresses or increase time on options')
        exit(0)
        return
    # Fill in username
    try:
        username = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.ID, 'username')))
        username.send_keys(usernameStr)
    except TimeoutException:
        logging.error('Username field could not be located!Perhaps element needed more time to load check options!')
        return

    # Fill in password
    try:
        password = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.ID, 'password')))
        password.send_keys(passwordStr)
    except TimeoutException:
        logging.error('Password field could not be located!')
        return

    # Hit sign in button
    try:
        nextButton = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.ID, 'signInBtn')))
        nextButton.click()
    except TimeoutException:
        logging.error('Sign in button could not be located!')
        return

     # Check if bot is logged in
    try:
        logged = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nav_home > a:nth-child(1)')))
    except TimeoutException:
        logging.error('Invalid Credentials! Username %s' , usernameStr)
        exit(0)


 #Set filters chosen
def setFilters(driver):
    
    logging.info('Setting filters...')

    # Locating filter button
    try: 
        browse_btn = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nav_people')))
    except TimeoutException:
        logging.info('Unable locate Browse button!')
        return

    browse_btn.click() # Click meet me button

     # Locating filter button
    try: 
        filter_btn = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.top-controls > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)')))
        filter_btn.click() # Click filters button
    except TimeoutException:
        logging.error('Unable locate filter button!')
        return

    
     # Locating filter options
    try: 
        WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH,  "//div[@class='row fields']")))
    except TimeoutException:
        logging.error('Filter popup never showed')
        return


    #Setting options
    try:
        gender  = Select(driver.find_element_by_css_selector('#browse > div:nth-child(2) > div > form > div > div > div.medium-10.columns > div > div.row.fields > div:nth-child(1) > div > select'))
        age_max = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR,  "input.age:nth-child(2)")))
        proximt = Select(driver.find_element_by_css_selector('#browse > div:nth-child(2) > div > form > div > div > div.medium-10.columns > div > div.row.fields > div:nth-child(5) > div > select'))

        gender.select_by_visible_text('Males')
        age_max.send_keys(Keys.CONTROL + "a")#and send values
        age_max.send_keys('60')
        proximt.select_by_visible_text('100 kilometers')
    except:
        logging.error('Unable to change filter settings!')
        return


     # Submiting FIlter options
    try: 
        submit = WebDriverWait(driver,AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR,  ".primary")))
        submit.click()
    except TimeoutException:
        logging.error('Filter submission button never showed up!')
        return

    logging.info('Succesfully changed filter options!')



def check_exists_by_css(driver,element):
    try:
        driver.find_element_by_css_selector(element)
    except NoSuchElementException:
       return False
    return True


 # Check whether a class element exists within or not
def check_exists_by_class(driver,element):
    try:
        driver.find_element_by_class_name(element)
    except NoSuchElementException:
       return False
    return True


# Likes as may people as there are
def likePeople(driver):
    logging.info('Start liking people...')
    visitUrl(driver,homepage)

    try: # Navigate to game
        meetme_btn = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nav_meetme')))
        meetme_btn.click() # Click meet me button
    except TimeoutException:
        logging.info('Unable to Navigate to Game!')
        return


    # Start liking people
    try:
        # For as long there are more people to like
        while(check_exists_by_css(driver,'div.meetme-buttons:nth-child(1) > form:nth-child(1) > div:nth-child(2) > button:nth-child(1)')):
             # Locate selector to like
            button = driver.find_element_by_css_selector('div.meetme-buttons:nth-child(1) > form:nth-child(1) > div:nth-child(2) > button:nth-child(1)')
            button.click() # Like 

            logging.info('Clicked like') # Log info

            button = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.meetme-buttons:nth-child(1) > form:nth-child(1) > div:nth-child(2) > button:nth-child(1)')))
    except:
        logging.warning('Failed to click like') # Log error



 # Go to Messages
def goToMessages(driver):

    visitUrl(driver,homepage) 
    logging.info('Going to messages ...!!')
    # Go to messages: 
    try:
        button = driver.find_element_by_css_selector('.nav_message > a:nth-child(1)')
        button.click() # Like 
        
    except:
        logging.error('Could not go to messages')
        return
    


 # Sends 1 message to each person from 'browse'
def messagePeople(driver):
    logging.info('Inside Message People Function...')
     # Go to gome page
    visitUrl(driver,homepage)

     # Go to browse
    try:
        button = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nav_people')))
        button.click()
    except TimeoutException:
        logging.error('Waiting for element took too much time !')
        return

     # Main window
    MAIN_WINDOW = driver.window_handles[0]
     #Do , for as long as next button can be clicked/found , after first loop of course
    while(check_exists_by_class(driver,'next')):
         # Failure to locate msg btn
        MSG_BTN_FAIL = False
        
         # Wait untill message button is present
        try:
            button = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH, "//div[@class='message']")))
        except TimeoutException:
            logging.error('Waiting for element took too much time !')
            MSG_BTN_FAIL = True

         # Elements are located properly / procceed
        if (not MSG_BTN_FAIL):
            
            try:
                mess_buttons = driver.find_elements_by_xpath("//div[@class='message']")
                mess_buttons.append(driver.find_elements_by_xpath("//div[@class='tagged-message-user']"))
                mess_buttons = driver.find_elements_by_xpath("//div[@title='Send Message']")
                mess_set = set(mess_buttons)
            except:
                logging.error('Unable to locate messaging buttons')
                return

            # For every button/friend to click/add
            for btn in mess_buttons:
                
                BOT_FAIL = False # If bot critically fails messaging , set to true
  
                # Try to click message button
                try:
                    driver.execute_script("arguments[0].click()", btn)
                except:
                    BOT_FAIL = True
                    logging.warn('Unable to locate send message button')
                    try:
                        driver.close() 
                        driver.switch_to_window(MAIN_WINDOW)
                        logging.info('Messaging window close succesfully') # Log
                    except:
                        logging.error('Unable to close widow!')
                        return

                
                # Bot has succesfully clicked o message button / procceed
                if ( not BOT_FAIL):
                    time.sleep(WAIT_FOR_POPUP_TIMER) # Wait for browser to load
                    # Try to switch window
                    logging.info('Switching to messaging window')
                    try:
                        # Switch to new window
                        message_window = driver.window_handles[1]
                        driver.switch_to_window(message_window) # Switch to message window
                    except:
                        BOT_FAIL = True # Bot fail :no open window / cant procceed
                        logging.error('Unable to open/switch new window')
                    
                    # Bot has succesfully opened new window/ proceed
                    if ( not BOT_FAIL):

                        try: # Waiting for txt input
                            convo = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH , "//ul[@class='ember-view conversation_container unstyled']")))
                            conversation = convo.text # Contains what has been said in chat
                            if (not conversation):
                                text_input = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#im_input')))
                                text_input.send_keys(GREET) 
                        except TimeoutException:
                            BOT_FAIL = True # Bot fail :no open window / cant procceed
                            driver.close() 
                            driver.switch_to_window(MAIN_WINDOW)
                            logging.error('Waiting for input field element took too much time !')
                            logging.info('Messaging window close succesfully') # Log
                        # Bot has succesfully written in txt_input/ proceed
                        if ( not BOT_FAIL):
    
                            # Send message
                            try:
                                send_button = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#im_send_button')))
                                send_button.click()
                            except:
                                logging.error('Waiting for send button element took too much time !')
                                BOT_FAIL = True
                                logging.info('Closing messaging window ...') # Log                              
                                handles = driver.window_handles # TO BE DELETE
                                logging.warn('Opened windows ' + str(len(handles))) # Log windows count
                                driver.close() 
                                driver.switch_to_window(MAIN_WINDOW)

                            if ( not BOT_FAIL):          
                                logging.info('Message sent succesfully') # Log
                                # Close driver and switch to main window
                                logging.info('Closing messaging window ...') # Log                              
                                handles = driver.window_handles # TO BE DELETE
                                logging.warn('Opened windows ' + str(len(handles))) # Log windows count
                                driver.close() 
                                driver.switch_to_window(MAIN_WINDOW)
                                logging.info('Messaging window close succesfully') # Log
                    
                  # For msg btn
        logging.info('Going to next page on Browse...')
        try:
            nxt = driver.find_element_by_class_name('next') # Find element next in order to click it
            nxt.click() # Click next
        except:
            logging.warning('Unable to go on Browse next page')
            break	


def replyBack(driver):
    logging.info('Going to Reply on Messages')
    goToMessages(driver)


    logging.info('Clicking on new')
    # Go to new: 
    try:
        button = driver.find_element_by_css_selector('li.tab:nth-child(2)')
        button.click() # Like 

        logging.info('Succesfully on Messages/New!!')
    except:
        logging.error('Could not go to Messages/New')
        return 
    


    # Reply to every message: 
    # Wait untill message button is present
    logging.info('Locating reply buttons..')
    try:
        WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Message"]'))) 
    except TimeoutException:
        logging.error('Waiting for element took too much time !')
        return

     # List containing all 'message' webelements to click 
    rply_buttons = driver.find_elements_by_xpath('//*[@title="Message"]')
    
    MAIN_WINDOW = driver.window_handles[0] # Main window

    logging.info('Start replying...')
     # For every button there is 
    for btn in rply_buttons:

        BOT_FAIL = False # If bot critically fails messaging , set to true


        # Try to click message button
        try:
            driver.execute_script("arguments[0].click()", btn)
        except:
            logging.warn('Unable to click on reply button')
            BOT_FAIL = True

    
        
         # Bot has succesfully clicked o message button / procceed
        if ( not BOT_FAIL):
            logging.info('Succesfully clicked on reply button')
            time.sleep(WAIT_FOR_POPUP_TIMER) # Wait for browser to load
            # Try to switch window
            logging.info('Switching to messaging window')
            try:
                # Switch to new window
                message_window = driver.window_handles[1]
                driver.switch_to_window(message_window) # Switch to message window
            except:
                BOT_FAIL = True # Bot fail :no open window / cant procceed
                logging.warn('Unable to open new window')
            
            # At this point
            # Bot has succesfully opened new window/ proceed
            if ( not BOT_FAIL):
                logging.info('Proccesing conversation..')
                try:
                    convo = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH , "//ul[@class='ember-view conversation_container unstyled']")))
                except:
                    logging.warn('Unable to read conversation')
                    
                conversation = convo.text # Contains what has been said in chat

                response = '' # Text as a response to reply

                for msg in reversed(messg):
                    if (not msg in conversation):
                        response = msg
                        

                # -----------------------------------------------------------------------

                logging.info('Replying...')
                try: # Waiting for txt input
                    text_input = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#im_input')))
                    text_input.send_keys(response) 
                except TimeoutException:
                    BOT_FAIL = True # Bot fail :no open window / cant procceed
                    if (len(handles) > 1):
                            driver.close() 
                            driver.switch_to_window(MAIN_WINDOW)
                            logging.info('Messaging window close succesfully') # Log
                    logging.warning('Unable to reply!Waiting for text field element took too much time !')
     
                 # Bot has succesfully written in txt_input/ proceed
                if ( not BOT_FAIL):

                    # Send reply
                    try:
                        send_button = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#im_send_button')))
                        send_button.click()
                    except: 
                        logging.error('Unable to reply!Waiting for send button element took too much time !')
                        BOT_FAIL = True
                        if (len(handles) > 1):
                            driver.close() 
                            driver.switch_to_window(MAIN_WINDOW)
                            logging.info('Messaging window close succesfully') # Log
                        logging.error('Waiting for element took too much time !')
                        

                    if ( not BOT_FAIL):
                            
                        time.sleep(3)
                        logging.info('Message sent succesfully') # Log

                        # Close driver and switch to main window
                        logging.info('Closing messaging window ...') # Log
     
                        logging.warn('Opened windows ' + str(len(handles))) # Log windows count

                        if (len(handles) > 1):
                            driver.close() 
                            driver.switch_to_window(MAIN_WINDOW)
                            logging.info('Messaging window close succesfully') # Log
                    
          # For msg btn

 # Does stuff
def doStuff(driver):
     # Bots life cycle /untill crash
    while True:
        likePeople(driver)      # Like recommended people
        messagePeople(driver)   # Messages  people
        replyBack(driver)       # Replies back to messages 
        time.sleep(BOT_CYCLE_SLEEP_TIMER)







