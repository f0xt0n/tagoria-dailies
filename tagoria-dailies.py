# Tagoria Dailies Completer

import random
from datetime import datetime, timedelta
from time import sleep
from splinter import Browser
import yaml

# Use Firefox extensions? Y/N (Must have "ublock_origin.xpi & "noscript.xpi")
try:
    browser = Browser('firefox', extensions=['ublock_origin.xpi', 'noscript.xpi'], capabilities={"acceptInsecureCerts": True})
    print ('[✅] Using Firefox with extensions.')
except:
    browser = Browser('firefox', capabilities={"acceptInsecureCerts": True})
    print ('[❌] Using Firefox without extensions.')

# Config
config = yaml.safe_load(open("config_priv.yml"))
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
# WIP - PLUNDER_LOCATION = config['PLUNDER_LOCATION']
AMBER_MAX = config['AMBER_MAX']

# Initial variable setup
days = 0
new_day = True
action_points = 6
quest_points = 3
stat_rotation = 1
quest_location = '/mountains/overview/zone/?w=1IN&thiszone=5' # Default location to plunder is Canyon
quest_complete = False
amber = 1


# Login
def login():
    if browser.links.find_by_href('/auth/loginform/'):
        print ('[*] Logging in..')
        browser.find_by_id('menuLink1').first.click()
        browser.find_by_name('world').select('1IN')
        browser.fill('username', USERNAME)
        browser.fill('password', PASSWORD)
        browser.find_by_name('LABEL_LOGIN').click()
        sleep(6)
    else:
        return
    return


# Collect Wages
def wages():
    if browser.is_element_present_by_id('leftNewsLink') and browser.is_element_present_by_xpath("//*[contains(@href,'/town/farm/?w=1IN')]"):
        browser.find_by_id('leftNewsLink').click()
        browser.find_by_name('ACTION_COLLECT_WAGE').click()
        return print ('[*] Collected wage from farm.')       
    else:
        return print ('[*] No wage to collect.')


# Work at Farm
def farm():
    global action_points
    global quest_points
    global new_day
    global days

    print ('[*] Going to Farm..')
    browser.find_by_id('menuLink4').click() # Go to Village
    sleep(3)
    browser.find_by_id('menuLink14').click() # Go to Farm in Village
    times_worked = 0
    while times_worked != 3:
        print ('[*] Working for 8 hours..')
        browser.find_by_name('workHoursSelectList').select('8')
        browser.find_by_name('ACTION_BEGIN_WORK').click()
        sleep(random.randint(10,21))
        print ('[*] Logging out..')
        browser.find_by_id('menuLink10').click() # Logout
        print ('[*] Zzz..')
        wait_until(8,random.randint(3,6),random.randint(3,52))
        print ("[*] Awaken! and claim what is yours..")
        login()
        wages()
        times_worked += 1
        print ('[*] Times worked: ' + str(times_worked))
    days +=1
    print ('[🌄] The sun rises once again. For ' + days + ' days, the legend continues..!')
    new_day = True
    action_points = 6
    quest_points = 3
    return


# Quest checks
def quest():
    global action_points
    global quest_points
    global quest_location
    global quest_complete  
    global new_day

    # Go to Druid
    print ('[*] Going to Druid..')
    browser.find_by_id('menuLink4').click() # Go to Village
    sleep(3)
    browser.find_by_id('menuLink11').click() # Go to Druid in Village
    sleep(3)
    browser.find_by_id('druid_mission').click()
    sleep(3)
    
    # Turn in quest
    if quest_complete:
        if browser.is_element_present_by_xpath("//*[contains(@id,'btn_complete_')]"):
            browser.find_by_xpath("//*[contains(@id,'btn_complete_')]").click()
            print ('[*] Turned in Quest.')
            sleep(3)
            browser.find_by_id('druid_mission').click()
            quest_complete = False
        else:
            print ('[*] No quest to turn in.')

    # Check if already have quest
    if browser.is_element_present_by_id('btn_abandon'):
        print ('[*] Quest already in progress.')

    # Get actual current Quest Points
    if browser.find_by_css('.mission_table2'):          
        xpathQP = '//*[@class="mission_table2"]/tbody/tr/th[text()="Quest points: "]/b'
        actualQP = int(browser.find_by_xpath(xpathQP).first.text)
        quest_points = actualQP        
        print ('[*] Quest Points: ' + str(quest_points))

    # Accept new quest
    # NOTE: accepts new quest before checking for AP so if we have any left over QP for the day, we can accept the quest for tomorrow and allow for them to effectively 'carry-over' to new day.
    if browser.links.find_by_href('/town/druid/accept/?w=1IN'):
        browser.links.find_by_href('/town/druid/accept/?w=1IN').click()
        sleep(3)        
        quest_complete = False

    # Check if we have any points
    if action_points == 0:
        new_day = False
        return print ('[*] No Action Points left, going to farm..')
    elif quest_points == 0:
        print ('[*] No Quest Points left, going to plunder..')

    # Determine quest location
    if browser.find_by_css('.mission_table'):
        location = browser.find_by_css('.mission_table').last
        if 'valley' in location.text:
            print ('[*] Quest location is: Valley')
            quest_location = '/mountains/overview/zone/?w=1IN&thiszone=1'
        elif 'river' in location.text:
            print ('[*] Quest location is: River')
            quest_location = '/mountains/overview/zone/?w=1IN&thiszone=2'
        elif 'ruins' in location.text:
            print ('[*] Quest location is: Ruins')
            quest_location = '/mountains/overview/zone/?w=1IN&thiszone=3'
        elif 'mine' in location.text:
            print ('[*] Quest location is: Mine')
            quest_location = '/mountains/overview/zone/?w=1IN&thiszone=4'
        elif 'canyon' in location.text:
            print ('[*] Quest location is: Canyon')
            quest_location = '/mountains/overview/zone/?w=1IN&thiszone=5'
        elif 'volcano' in location.text:
            print ('[*] Quest location is: Volcano')
            quest_location = '/mountains/overview/zone/?w=1IN&thiszone=6'
        else:
            print ('[*] No quest active, going to Canyon..')
            quest_location = '/mountains/overview/zone/?w=1IN&thiszone=5'
    
    plunder()
    return


# Begin Quest or Plunder Location until run out of Action Points
def plunder():
    global action_points
    global quest_complete
    global amber

    browser.find_by_id('menuLink5').click() # Go to Mountains
    browser.links.find_by_href(quest_location).click() # Go to Quest Location
    quest_complete = False

    while action_points != 0 and not quest_complete:
        if browser.is_element_present_by_name('MISSION_BUTTON'):
            action = 'MISSION_BUTTON'
            print ('[*] Attempting Quest..')
        elif browser.is_element_present_by_name('EXPLORATION_BUTTON'):
            action = 'EXPLORATION_BUTTON'
            print ('[*] Attempting Quest..')
        elif browser.is_element_present_by_name('PLUNDER_BUTTON'):
            action = 'PLUNDER_BUTTON'
            print ('[*] Plundering..')

        while not quest_complete: # Attempts quest until succeeds or runs out of Action Points                
            # Get actual current Action Points
            if browser.find_by_css('.buy_action_point_table'):            
                xpathAP = '//*[@class="buy_action_point_table"]/tbody/tr/td/b'
                actualAP = int(browser.find_by_xpath(xpathAP).first.text)
                action_points = actualAP
                print ('[*] Action Points: ' + str(action_points))
            if action_points == 0:
                break            
            browser.find_by_name(action).click()
            print ('[*] Battling..')
            wait_until(0,10,random.randint(25,46)) # Wait 10 mins 25-45 secs
            if browser.is_text_present('Winner: ' + USERNAME):                
                print ('[*] Victory!')
                print ('--------------------')
            else:
                print ('[*] Defeat!')
                print ('--------------------')
            if browser.is_text_present('Well done! You have accomplished your task.') or browser.is_text_present('You have successfully explored the region.'):                    
                print ('[*] Quest Complete.')
                print ('--------------------')
                quest_complete = True
                sleep(9)
            else:
                browser.links.find_by_href(quest_location).click()
            # Check if levelled up
            levelup()
            # Check if at amber threshold
            skiller()   
    return


# Check if levelled up
def levelup():    
    if browser.is_element_present_by_id('leftNewsLink') and browser.links.find_by_href('/char/attributes/levelup/?w=1IN'):
        # browser.is_element_present_by_xpath("//*[contains(@href,'/town/levelup/?w=1IN')]")
        print ('[*] Collecting levelup reward..')
        browser.find_by_id('leftNewsLink').click()
        #browser.find_by_name('ACTION_COLLECT_LEVELUP').click()
        browser.links.find_by_href('/char/attributes/levelup/?w=1IN&1738627445&collect=1').click()  # ||Issue: Unsure if general link or unique to certain level?
        sleep(9)
    else:
        return
    return


# Increase attributes in sequence
def skiller():
    global stat_rotation
    global amber
   
    browser.find_by_id('menuLink1').click() # Go to Character Stats

    # Buy skillpoints
    buySP()

    # Spend skillpoints on stats in rotation until depleted
    print ('[*] Increasing attributes..')
    while not browser.is_text_present('insufficient'):
        if stat_rotation == 1:
            browser.find_by_id('incr_str').click() # Increase Strength
            sleep(3)
            stat_rotation += 1
        elif stat_rotation == 2:
            browser.find_by_id('incr_dex').click() # Increase Dexterity
            sleep(3)
            stat_rotation += 1
        elif stat_rotation == 3:
            browser.find_by_id('incr_agi').click() # Increase Agility
            sleep(3)
            stat_rotation += 1
        elif stat_rotation == 4:
            browser.find_by_id('incr_sta').click() # Increase Stamina
            sleep(3)
            stat_rotation = 1
        else:
            break
    return


def buySP():   
    # Get current Amber
    if browser.find_by_id('spMoney'):
        amber = int(browser.find_by_id('spMoney').first.text)
    # Buy skillpoints until under Amber threshold
    print ('[*] Amber: ' + str(amber) + ' / ' + str(AMBER_MAX))
    if amber > AMBER_MAX:
        print ('[*] Buying skillpoints..')
        while amber > AMBER_MAX:
            browser.find_by_id('buy_SP').click() # Purchase Skillpoints
            sleep(3)
            amber = int(browser.find_by_id('spMoney').first.text)
        print ('[*] Amber: ' + str(amber) + ' / ' + str(AMBER_MAX))
    else:
        print ('[*] Amber under threshold.')
    return


# Wait
def wait_until(hours,minutes,seconds):
    future = datetime.replace(datetime.now() + timedelta(hours=hours,minutes=minutes,seconds=seconds))
    print ('[*] Completion : ' + str(future))
    while True:
        diff = (future - datetime.now()).total_seconds()
        # Increased precision
        if diff <= 0:
            return
        elif diff <= 0.1:
            sleep(0.001)
        elif diff <= 0.5:
            sleep(0.01)
        elif diff <= 1.5:
            sleep(0.1)
        else:
            sleep(1)


# Error Handling - lol
def error():
    print ('[!!] Error [!!]')
    sleep(9)
    browser.find_by_id('menuLink10').click() # Logout
    return



# Entry
print ('--~={| Initiate Tagoria Dailies Completer |}=~--')
browser.visit('https://www.tagoria.net/?lang=en')
while True:
    login()
    wages()
    while new_day:
        quest()
    farm()


# Forseen Issues::
# - Eventually the midnight points reset might intersect with when script is active doing quests/plundering. 
# - This will desync points value stored in code and actual points, resulting in script not using up all points for the day.
# - 1 day skip inefficiency :'(
