import csv, difflib, functions, logging, PIL, psutil, pytesseract, sqlite3, subprocess, threading, win32gui, win32process

from psutil import NoSuchProcess

# Logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(funcName)-30s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
pytesseract.pytesseract.tesseract_cmd = "E:/sbilal/Logiciels/Tesseract-OCR/tesseract.exe"

class Character:
    def __init__(self, name: str) -> None:
        self.name = name
        
        database = sqlite3.connect("db/genshin.sqlite3")
        cursor = database.execute("SELECT * FROM characters WHERE en_name='" + self.name + "'").fetchall()[0]
        self.vision = cursor[4]
        self.skill = cursor[5]
        self.burst = cursor[6]
        database.close()
        # self.level = [None, None]
        # self.max_hp = [None, None]
        # self.atk = [None, None]
        # self.defense = [None, None]
        # self.elemental_mastery = None
        # self.max_stamina = None
        # self.crit_rate = None
        # self.crit_dmg = None
        # self.healing_bonus = None
        # self.incoming_healing_bonus = None
        # self.energy_recharge = None
        # self.cd_reduction = None
        # self.shield_strengh = None
        # self.pyro_dmg_bonus = None
        # self.pyro_res = None
        # self.hydro_dmg_bonus = None
        # self.hydro_res = None
        # self.dendro_dmg_bonus = None
        # self.dendro_res = None
        # self.electro_dmg_bonus = None
        # self.electro_res = None
        # self.anemo_dmg_bonus = None
        # self.anemo_res = None
        # self.cryo_dmg_bonus = None
        # self.cryo_res = None
        # self.geo_dmg_bonus = None
        # self.geo_res = None
        # self.physical_dmg_bonus = None
        # self.physical_res = None

    def get_gacha_card_image(self) -> PIL.Image:
        return PIL.Image.open(functions.script_path + "/img/Multi-Wish arts/" + self.name + ".png")
    
    def get_skill_icon(self) -> PIL.Image:
        filename = self.skill.replace(":", "")
        return PIL.Image.open(functions.script_path + "/img/Talent icons/" + filename + ".png")

    def get_burst_icon(self) -> PIL.Image:
        filename = self.burst.replace(":", "")
        return PIL.Image.open(functions.script_path + "/img/Talent icons/" + filename + ".png")

    
    def set_page1_stats(self, stats_list: list):
        self.max_hp = [stats_list[0], stats_list[1]]
        self.atk = [stats_list[2], stats_list[3]]
        self.defense = [stats_list[4], stats_list[5]]
        self.elemental_mastery = stats_list[6]
        self.max_stamina = stats_list[7]
        self.crit_rate = stats_list[8]
        self.crit_dmg = stats_list[9]
        self.healing_bonus = stats_list[10]
        self.incoming_healing_bonus = stats_list[11]
        self.energy_recharge = stats_list[12]
        self.cd_reduction = stats_list[13]
        self.shield_strengh = stats_list[14]

# Launch-related functions
def is_game_open() -> bool:
    '''Returns True if Genshin Impact is currently open. False otherwise.'''
    output = str(subprocess.check_output("tasklist", shell=True))
    return "GenshinImpact.exe" in output

def is_game_active() -> bool:
    '''Returns True if Genshin Impact is the current active window. False otherwise.'''
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    try:
        active_name = psutil.Process(pid[-1]).name()
        if active_name == "GenshinImpact.exe":
            logging.info("Genshin Impact is the current active window.")
            return True
    except NoSuchProcess:
        pass
    logging.info("Genshin Impact is not the current active window.")
    return False

# Screenshot-related functions
def screenshot(x: int, y: int, width: int, height: int) -> PIL.Image:
    '''Screenshots Genshin Impact at set coordinates and returns Image.'''
    def get_genshin_window_coordinates() -> tuple:
        '''Returns x and y coordinates of the Genshin Impact window, alongside its width and height.'''
        hwnd = win32gui.FindWindow(None, "Genshin Impact")
        return win32gui.GetWindowRect(hwnd)
    window_x, window_y, window_width, window_height = get_genshin_window_coordinates()
    return functions.get_screenshot(window_x + x + 3, window_y + y + 26, width, height) # "+ 26" to account for title bar size (for 1920x1080)

def pixel_color(x: int, y: int) -> int:
    '''Returns color of pixel at set coordinates.'''
    return screenshot(x, y, 1, 1).getpixel((0, 0))

def get_party_icons() -> PIL.Image:
    x = 1751
    y1, y2, y3, y4  = 219, 315, 411, 507
    width, height = 104, 80
    character_1 = screenshot(x, y1, width, height)
    character_2 = screenshot(x, y2, width, height)
    character_3 = screenshot(x, y3, width, height)
    character_4 = screenshot(x, y4, width, height)
    return (character_1, character_2, character_3, character_4)

# Genshin Impact-related functions
def get_party_members() -> list:
    '''Returns list of Character object containing current party.'''
    party = {}
    x = 1624
    y = (244, 340, 436, 532)
    width, height = 139, 43
    def get_party_member(index: int, y: int):
        character_name = None
        while character_name == None:
            image = screenshot(x, y, width, height)
            character_name = read_character_name(image)
        character = Character(character_name)
        party[index] = character
    
    threads = []
    for i in range(0, len(y)):
        threads.append(threading.Thread(target=get_party_member, args=(i + 1, y[i])))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return party

def get_current_character() -> int:
    '''Returns index of current played character. Returns 0 if it fails.'''
    party_color = (
        pixel_color(1882, 268), 
        pixel_color(1882, 364), 
        pixel_color(1882, 460), 
        pixel_color(1882, 556)
    )
    for i in range(0, 4):
        if party_color[i] != (255, 255, 255):
            logging.info(str(i + 1) + " is the current character.")
            return i + 1
    logging.info("No current character found.")
    return 0

def get_health_points() -> tuple:
    '''Returns the current character's health points out of its maximum. Returns (0, 0) if there is nothing to read or fails to read it.'''
    def get_health_points_screenshot() -> PIL.Image:
        x, y = 894, 1002
        width, height = 132, 17
        return screenshot(x, y, width, height)
    image1 = get_health_points_screenshot()
    health = functions.image_to_str(image1, "[^0-9. /]")
    logging.info(health + " readen.")
    try:
        health = health.split("/")
        health = (int(health[0]), int(health[1]))
        logging.info("Current's character health is " + str(health) + ".")
        return health
    except (ValueError, IndexError):
        return (0, 0)

def get_skill_cd() -> float:
    '''Returns cooldown of the current character's skill. Returns 0.0 if there is nothing to read or fails to read it.'''
    def get_skill_cd_screenshot() -> PIL.Image:
        x, y = 1663, 981
        width, height = 58, 22
        return screenshot(x, y, width, height)
    image1 = get_skill_cd_screenshot()
    timer = functions.image_to_str(image1, "[^0-9. ]")
    logging.info(timer + " readen.")
    try:
        timer = float(timer)
        logging.info("A skill has been used. Remaining time of " + str(timer) + "seconds.")
        return timer
    except ValueError:
        return 0.0

def read_character_name(image: PIL.Image) -> str:
    '''Returns character name from a screenshot. None if it fails.'''
    def get_character_list() -> list:
        '''Returns a list of str containing all Genshin Impact characters name.'''
        character_list = []
        database = sqlite3.connect("db/genshin.sqlite3")
        cursor = database.execute("SELECT en_name FROM characters")
        list = cursor.fetchall()
        for item in list:
            character_list.append(item[0])
        database.close()
        return character_list
    readen_text = functions.image_to_str(image, '[^a-zA-Z. ]')
    try:
        match = difflib.get_close_matches(readen_text, get_character_list(), n = 1, cutoff = 0.7)[0]
        logging.info("\"" + readen_text + "\" readen, match with \"" + match + "\"")
        return match
    except IndexError:
        logging.info("\"" + readen_text + "\" readen, could not match with any character name.")
        return None

def get_character_page_name() -> Character:
    character_name = None
    x, y = 142, 21
    width, height = 340, 56
    while character_name == None:
        character_name = read_character_name(screenshot(x, y, width, height))
    return Character(character_name)

def get_page1_stats():
    x1, y1, x2, y2 = 1200, 100, 1470, 320
    y3, y4 = 500, 1030
    screenshot1 = screenshot(x1, y1, x2, y2)
    stats1 = functions.image_to_str(screenshot1, '[^0-9\n ]')
    screenshot2 = screenshot(x1, y3, x2, y4)
    stats2 = functions.image_to_str(screenshot2, '[^0-9,\n. ]')
    return (stats1 + stats2).split()