from PIL import Image, ImageEnhance, ImageGrab, ImageQt
from PyQt5.QtCore import QBuffer, QIODevice, QPoint
from PyQt5.QtGui import QImage, QPixmap, qRgb
import ctypes, cv2, io, logging, numpy, pytesseract, re, sys, win32api

def darken_pixmap(pixmap: QPixmap, factor: float) -> Image:
    image = pixmap.toImage()
    for h in range(0, image.height()):
        for w in range(0, image.width()):
            color = image.pixelColor(w, h)
            if (image.pixel(w, h) != 0):
                color.setRgb(color.red() * factor, color.blue() * factor, color.green() * factor, color.alpha())
                image.setPixelColor(w, h, color)

    return QPixmap.fromImage(image)

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def get_screenshot(x: int, y: int, width: int, height: int) -> Image:
    logging.info("Taking screenshot: (x1 = " + str(x) + ", y1 = " + str(y) + ", x2 = " + str(width) + ", y2 = " + str(height) + ")")
    box = (x, y, width, height)
    image = ImageGrab.grab(bbox = box)
    return image

def image_to_str(image: Image) -> str:
    cv2_image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    cv2_image = get_grayscale(cv2_image)
    custom_config = r'--oem 3 --psm 6'
    str = pytesseract.image_to_string(cv2_image, config=custom_config)
    regex = re.compile('[^a-zA-Z0-9. ]')
    str = regex.sub('', str)
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
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit(0)