from selenium import webdriver
from time import sleep
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def find_duplicate(list, element):
    for i in range(len(list)):
        if list[i][0] == element:
            return True
    return False

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Driver\chromedriver.exe', chrome_options=options)
input_class = input("Enter class (ex death-knight): ")
list_class = ["death-knight", "demon-hunter", "druid", "hunter", "mage", "monk", "paladin", "priest", "rogue", "shaman", "warlock", "warrior"]
if find_duplicate(list_class, input_class):
    print("Class not found")
    sleep(3)
    driver.quit()
input_spec = input("Enter spec (ex blood): ")
input_game = input("Enter game (ex wotlk, retail, classic): ")
if input_game == "wotlk":
    url = "https://www.wowhead.com/wotlk/spells/abilities/" + input_class + "/" + input_spec
elif input_game == "retail":
    url = "https://www.wowhead.com/spells/abilities/" + input_class + "/" + input_spec
elif input_game == "classic":
    url = "https://classic.wowhead.com/spells/abilities/" + input_class + "/" + input_spec
else:
    print("Invalid game")
    sleep(3)
    driver.quit()
print(url)
driver.get(url)
rows = driver.find_elements_by_class_name("listview-mode-default")[0].find_elements_by_tag_name("tr")
list = []
for row in rows[1:]:
    skill_name = row.find_elements_by_class_name("listview-cleartext")[0].text
    skill_name = ''.join(e for e in skill_name if e.isalnum() or e == " ")
    is_passive = False
    is_higher_rank = False
    small_text = row.find_elements_by_class_name("small2") 
    if small_text:
        is_passive = small_text[0].text == "Passive"
        is_higher_rank = int(small_text[0].text[-1]) > 1 if small_text[0].text[-1].isdigit() else False
    if find_duplicate(list, skill_name) or is_passive or is_higher_rank:
        continue
    skill_id = row.find_elements_by_tag_name("a")[0].get_attribute("href")
    skill_id = skill_id.split("=")[1].split("/")[0]
    list.append([skill_name, skill_id])
for i in range(len(list)):
    print('private string ' + list[i][0].replace(" ", "") + ' = "' + list[i][0] + '";')
print("\n")
for i in range(len(list)):
    print('AddSpell(' + list[i][0].replace(" ", "") + ', ' + list[i][1] + ', "None");')
input("Press enter to exit")
driver.quit()