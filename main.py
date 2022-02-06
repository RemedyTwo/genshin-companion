from xml.dom.minidom import Attr
from PIL import ImageEnhance, ImageQt
import functions, genshin, logging, pynput, PyQt5, PyQt5.QtCore, time, gui.user_interface, sys

class GameState(PyQt5.QtCore.QThread):
    game_active = PyQt5.QtCore.pyqtSignal()
    game_inactive = PyQt5.QtCore.pyqtSignal()
    state = False

    def run(self) -> None:
        while not self.isInterruptionRequested():
            while self.state:
                if not genshin.is_game_active():
                    self.game_inactive.emit()
                    self.state = False
                time.sleep(5)
            while not self.state:
                if genshin.is_game_active():
                    self.game_active.emit()
                    self.state = True
                time.sleep(10)

class Game(PyQt5.QtCore.QThread):
    gameplay = PyQt5.QtCore.pyqtSignal()
    burst = PyQt5.QtCore.pyqtSignal()
    character_menu = PyQt5.QtCore.pyqtSignal()
    stats_page1 = PyQt5.QtCore.pyqtSignal()
    stats_page2 = PyQt5.QtCore.pyqtSignal()
    last_state = None

    def run(self) -> None:
        while not self.isInterruptionRequested():
            if not self.last_state == self.gameplay and genshin.pixel_color(1570, 50) == (255, 255, 255):
                self.gameplay.emit()
                self.last_state = self.gameplay
            elif not self.last_state == self.character_menu and genshin.pixel_color(80, 1000) == (59, 66, 85):
                self.character_menu.emit()
                self.last_state = self.character_menu
            elif not self.last_state == self.stats_page1 and genshin.pixel_color(225, 90) == (255, 255, 255):
                self.stats_page1.emit()
                self.last_state = self.stats_page1
            elif not self.last_state == self.stats_page2 and genshin.pixel_color(225, 950) == (255, 255, 255):
                self.stats_page2.emit()
                self.last_state = self.stats_page2
            else:
                self.burst.emit()
            time.sleep(10)
        
class CharacterSwitch(PyQt5.QtCore.QThread):
    current_character = PyQt5.QtCore.pyqtSignal(int)
    last_current_character = 0

    def run(self) -> None:
        self.listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()
    
    def requestInterruption(self) -> None:
        self.listener.stop()
        return super().requestInterruption()

    def on_press(self, key) -> None:
        try:
            button_pressed = key.char
        except AttributeError:
            return
        if button_pressed == '&' or button_pressed == 'é' or button_pressed == '"' or button_pressed == "'":
            time.sleep(0.1)
            current_character = genshin.get_current_character()
            if not current_character == 0 and not current_character == self.last_current_character:
                self.current_character.emit(current_character)
                self.last_current_character = current_character

class Health(PyQt5.QtCore.QThread):
    health_points = PyQt5.QtCore.pyqtSignal(int, int)

    def run(self) -> None:
        while not self.isInterruptionRequested():
            health = genshin.get_health_points()
            if not health == (0, 0):
                self.health_points.emit(health[0], health[1])
            time.sleep(2)
    
class Skill(PyQt5.QtCore.QThread):
    skill_cooldown = PyQt5.QtCore.pyqtSignal(float)

    def run(self) -> None:
        self.listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()
    
    def requestInterruption(self) -> None:
        self.listener.stop()
        return super().requestInterruption()

    def on_press(self, key) -> None:
        try:
            button_pressed = key.char
        except AttributeError:
            return
        if button_pressed == 'E' or button_pressed == 'e':
            skill_cooldown = genshin.get_skill_cd()
            if not skill_cooldown == 0.0:
                self.skill_cooldown.emit(skill_cooldown)

class Burst(PyQt5.QtCore.QThread):
    burst_cooldown = PyQt5.QtCore.pyqtSignal(float)

    def run(self) -> None:
        self.listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()
    
    def requestInterruption(self) -> None:
        self.listener.stop()
        return super().requestInterruption()

    def on_press(self, key) -> None:
        try:
            button_pressed = key.char
        except AttributeError:
            return
        if button_pressed == 'A' or button_pressed == 'a':
            burst_cooldown = genshin.get_skill_cd()
            if not burst_cooldown == 0.0:
                self.burst_cooldown.emit(burst_cooldown)

class Timer(PyQt5.QtCore.QThread):
    def __init__(self, field, cooldown: float) -> None:
        super().__init__()
        self.field = field
        self.cooldown = cooldown

    def run(self) -> None:
        current_time = time.time()
        final_time = current_time + self.cooldown
        while final_time > time.time() and not self.isInterruptionRequested():
            cooldown_text = str(round(final_time - time.time(), 1))
            self.field.setText(cooldown_text)
            time.sleep(0.1)
        self.field.setText("")

class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ui = gui.user_interface.Ui_MainWindow()
        self.ui.setupUi(self)   
        self.multiwish_art = (self.ui.multiwish_art_1, self.ui.multiwish_art_2, self.ui.multiwish_art_3, self.ui.multiwish_art_4)
        self.health = (self.ui.health_1, self.ui.health_2, self.ui.health_3, self.ui.health_4)
        self.burst_art = (self.ui.burst_art_1, self.ui.burst_art_2, self.ui.burst_art_3, self.ui.burst_art_4)
        self.skill_art = (self.ui.skill_art_1, self.ui.skill_art_2, self.ui.skill_art_3, self.ui.skill_art_4)
        self.skill_cooldown = (self.ui.skill_cooldown_1, self.ui.skill_cooldown_2, self.ui.skill_cooldown_3, self.ui.skill_cooldown_4)

        # Memory
        self.current_character = 0

        # Game state
        self.game_state = GameState()
        self.game_state.start()
        self.game_state.game_active.connect(self.game_now_active)
        self.game_state.game_inactive.connect(self.game_now_inactive)

        # Other threads
        self.skill_cd_threads = {}
        self.burst_cd_threads = {}

    def game_now_active(self) -> None:
        self.game = Game()
        self.game.gameplay.connect(self.now_in_gameplay)
        self.game.character_menu.connect(self.now_in_character_menu)
        self.game.start()

    def game_now_inactive(self) -> None:
        self.health_thread.requestInterruption()
        self.skill_thread.requestInterruption()
        self.burst_thread.requestInterruption()
        self.game.requestInterruption()
        for _, skill_cd_thread, _, burst_cd_thread in zip(self.skill_cd_threads.items(), self.burst_cd_threads.items()):
            skill_cd_thread.requestInterruption()
            burst_cd_thread.requestInterruption()

    def now_in_gameplay(self) -> None:
        self.character_switch_thread = CharacterSwitch()
        self.character_switch_thread.current_character.connect(self.update_current_character)

        self.health_thread = Health()
        self.health_thread.health_points.connect(self.update_health)

        self.skill_thread = Skill()
        self.skill_thread.skill_cooldown.connect(self.update_skill_cd)

        self.burst_thread = Burst()
        self.burst_thread.burst_cooldown.connect(self.update_burst_cd)

        self.character_switch_thread.start()
        self.health_thread.start()
        self.skill_thread.start()
        self.burst_thread.start()

        self.update_party()
        logging.info("Currently in gameplay.")
    
    def now_in_character_menu(self) -> None:
        self.health_thread.requestInterruption()
        self.skill_thread.requestInterruption()
        self.burst_thread.requestInterruption()
        name = genshin.get_character_page_name().name
        logging.info("Currently in " + name + " character menu")

    def update_party(self) -> None:
        darken_factor = 0.5
        icon_size = 64

        self.party = genshin.get_party_members()
        for i in range(0, 4):
            character_art = self.party.get(i + 1).get_multiwish_art()
            skill_art = ImageQt.toqpixmap(self.party.get(i + 1).get_skill_icon()).scaledToWidth(icon_size)
            burst_art = ImageQt.toqpixmap(self.party.get(i + 1).get_burst_icon()).scaledToWidth(icon_size)
            if not i + 1 == self.current_character:
                enhancer = ImageEnhance.Brightness(character_art)
                character_art = enhancer.enhance(darken_factor)
            self.multiwish_art[i].setPixmap(ImageQt.toqpixmap(character_art))
            self.skill_art[i].setPixmap(skill_art)
            self.burst_art[i].setPixmap(burst_art)

    def update_current_character(self, current_character: int) -> None:
        darken_factor = 0.5
        self.current_character = current_character

        for i in range(0, 4):
            character_art = self.party.get(i + 1).get_multiwish_art()
            if not i + 1 == self.current_character:
                enhancer = ImageEnhance.Brightness(character_art)
                character_art = enhancer.enhance(darken_factor)
            self.multiwish_art[i].setPixmap(ImageQt.toqpixmap(character_art))
    
    def update_health(self, current_hp: int, max_hp: int) -> None:
        text = str(current_hp) + " / " + str(max_hp)
        self.health[self.current_character - 1].setText(text)
        logging.info("TODO, update health")
        pass
    
    def update_skill_cd(self, cooldown: float) -> None:
        if self.current_character == 0:
            logging.info("Current character is not known.")
            return

        field = self.skill_cooldown[self.current_character - 1]
        cooldown = Timer(field, cooldown)
        if not self.skill_cd_threads.get(self.current_character) is None:
            self.skill_cd_threads.get(self.current_character).requestInterruption()

        self.skill_cd_threads[self.current_character] = cooldown
        self.skill_cd_threads.get(self.current_character).start()

    def update_burst_cd(self, cooldown: float) -> None:
        if self.current_character == 0:
            logging.info("Current character is not known.")
            return

        field = self.burst_cooldown[self.current_character - 1]
        cooldown = Timer(field, cooldown)
        if not self.burst_cd_threads.get(self.current_character) is None:
            self.burst_cd_threads.get(self.current_character).requestInterruption()

        self.burst_cd_threads[self.current_character] = cooldown
        self.burst_cd_threads.get(self.current_character).start()

if __name__ == "__main__":
    if not functions.is_admin():
        functions.launch_as_admin()
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())