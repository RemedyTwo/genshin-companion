from functions import *
from PIL import Image
import difflib, logging, psutil, pytesseract, subprocess, time, win32gui, win32process
    
GENSHIN_ACTIVE = None

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
pytesseract.pytesseract.tesseract_cmd = "E:\\sbilal\\Logiciels\\Tesseract-OCR\\tesseract.exe"

class Character:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def get_gacha_card_image(self) -> Image:
        return Image.open("E:\\sbilal\\Code\\genshin-overlay\\img\\" + self.name + ".png")

# Launch-related functions
def is_game_open() -> bool:
    output = str(subprocess.check_output("tasklist", shell=True))
    if "GenshinImpact.exe" in output:
        return True
    return False

def is_game_active() -> bool:
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow()) 
    active_window = psutil.Process(pid[-1]).name()
    global GENSHIN_ACTIVE
    if active_window == "GenshinImpact.exe":
        if not GENSHIN_ACTIVE == True:
            logging.info("Genshin Impact is the current active window.")
            GENSHIN_ACTIVE = True
        return True
    else:
        if not GENSHIN_ACTIVE == False:
            logging.info("Genshin Impact is not the current active window.")
            GENSHIN_ACTIVE = False
        return False

# Screenshot-related functions 1620 270 1765 600
def get_genshin_screenshot(x1: int, y1: int, x2: int, y2: int) -> Image:
    x, y, w, h = get_genshin_window_coordinates()
    return get_screenshot(x + x1, y + y1, x + x2, y + y2)

def get_genshin_window_coordinates() -> tuple:
    hwnd = win32gui.FindWindow(None, "Genshin Impact")
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    width = rect[2]
    height = rect[3]
    return x, y, width, height

def get_party_screenshot() -> Image:
    character1 = get_genshin_screenshot(1620, 260, 1765, 305)
    character2 = get_genshin_screenshot(1620, 360, 1765, 405)
    character3 = get_genshin_screenshot(1620, 460, 1765, 505)
    character4 = get_genshin_screenshot(1620, 560, 1765, 605)
    return (character1, character2, character3, character4)

def get_skill_cd_screenshot() -> Image:
    return get_genshin_screenshot(1670, 1005, 1720, 1030)

# Genshin Impact-related functions
def is_character_switched() -> bool:
    if not is_key_pressed("1") and not is_key_pressed("2") and not is_key_pressed("3") and not is_key_pressed("4"):
        return False
    logging.info("Character switch attempt recognized.")
    time.sleep(0.5)
    current_character = get_current_character()
    logging.info("Current character: " + str(current_character))

def is_skill_used() -> bool:
    if not is_key_pressed('E'):
        return False
    logging.info("'E' input recognized.")
    for _ in range(0, 5):
        image1 = get_skill_cd_screenshot()
        timer = image_to_str(image1)
        logging.info("Readen number: " + str(timer))
        try:
            float(timer)
            logging.info("A skill has been used.")
            return True
        except ValueError:
            logging.info("A skill has not been used.")
    return False

def get_character_list() -> list:
    with open("db/character_list.txt") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def get_current_character() -> int:
    character1 = get_genshin_screenshot(1882, 300, 1883, 301)
    character2 = get_genshin_screenshot(1882, 395, 1883, 396)
    character3 = get_genshin_screenshot(1882, 490, 1883, 491)
    character4 = get_genshin_screenshot(1882, 585, 1883, 586)
    party_color = (character1.getpixel((0, 0)), character2.getpixel((0, 0)), character3.getpixel((0, 0)), character4.getpixel((0, 0)))
    amount = 0
    for i in range(0, 4):
        if party_color[i] != (255, 255, 255):
            current = i
            amount += 1
    if amount > 1:
        return 0
    return current + 1

def get_character_from_name(image: Image) -> str:
    character_attempt = image_to_str(image)
    print("Name readen = " + character_attempt)
    try:
        return difflib.get_close_matches(character_attempt, get_character_list(), n = 1, cutoff=0.6)[0]
    except IndexError:
        return None
        
def get_character_from_avatar(image: Image) -> str:
    pass

def get_party_members_from_name() -> list:
    party = []
    x1, y1, x2, y2 = 1620, 260, 1765, 305
    for i in range (0, 4):
        character = Character(None)
        while(character.name == None or 4 > len(character.name)):
            screenshot = get_genshin_screenshot(x1, y1, x2, y2)
            character = Character(get_character_from_name(screenshot))
        party.append(character)
        y1 += 100
        y2 += 100
    return party

def get_party_members_from_avatar() -> list:
    pass

def main():
    launch_as_admin()
    if not is_game_open():
        exit(0)
    party = []
    while(len(party) == 0):
        party = get_party_members_from_name()
        logging.info("Current party members: " + str(party))
    while True:
        while not is_game_active():
            time.sleep(5)
        if is_skill_used():
            pass
        if is_character_switched():
            pass
            
if __name__ == "__main__":
    main()