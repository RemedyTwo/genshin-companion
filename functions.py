from PIL import Image, ImageGrab
import ctypes, cv2, logging, numpy, os, PyQt5.QtGui, pytesseract, re, sys, win32api

script_path = os.path.dirname(__file__)

def darken_pixmap(pixmap: PyQt5.QtGui.QPixmap, factor: float) -> Image:
    image = pixmap.toImage()
    for h in range(0, image.height()):
        for w in range(0, image.width()):
            color = image.pixelColor(w, h)
            if (image.pixel(w, h) != 0):
                color.setRgb(color.red() * factor, color.blue() * factor, color.green() * factor, color.alpha())
                image.setPixelColor(w, h, color)

    return PyQt5.QtGui.QPixmap.fromImage(image)

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def get_screenshot(x: int, y: int, width: int, height: int) -> Image:
    logging.info("Taking screenshot: (x = " + str(x) + ", y = " + str(y) + ", width = " + str(width) + ", height = " + str(height) + ")")
    return ImageGrab.grab((x, y, x + width, y + height))

def image_to_str(image: Image, regex: str) -> str:
    cv2_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    cv2_image = get_grayscale(cv2_image)
    custom_config = r'--oem 3 --psm 6'
    str = pytesseract.image_to_string(cv2_image, config=custom_config)
    regex = re.compile(regex)
    str = regex.sub('', str).strip()
    return str

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_key_pressed(key: str) -> bool:
    value = win32api.GetAsyncKeyState(ord(key))
    if value == 0:
        return False
    return True

def launch_as_admin() -> None:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    exit(0)