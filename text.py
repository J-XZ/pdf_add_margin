import subprocess
from time import sleep
from pynput import keyboard
import keyboard as kb
from datetime import datetime
import threading
from time import sleep
from pynput import keyboard
import keyboard as kb
from datetime import datetime
import threading
import pyautogui
import random


def mo():
    # 监测鼠标是否晃动，如果连续5秒没有晃动，就持续随机晃动鼠标。在晃动鼠标的过程中，如果鼠标被移动，就立刻停止晃动，并且等待5秒后再次开始晃动。
    # 用于防止电脑休眠

    interval = 5 * 60  # in seconds
    # interval = 5  # in seconds

    last_position = [None, None]

    def check_mouse_movement():
        nonlocal last_position
        nonlocal interval
        current_position = pyautogui.position()
        if last_position == current_position:
            shake_mouse()
        else:
            last_position = current_position
            # Restart the timer
            threading.Timer(interval, check_mouse_movement).start()

    def shake_mouse():
        print("Start Shaking")
        nonlocal last_position
        current_position = pyautogui.position()
        if last_position == current_position:
            # Mouse has not moved, start shaking
            while last_position == current_position:
                try:
                    pyautogui.move(
                        random.randint(-1, 1), random.randint(-1, 1), duration=0
                    )
                except:
                    # move to center
                    pyautogui.moveTo(960, 540, duration=0.2)
                    pass
                # Restart the timer
                current_position = pyautogui.position()
                if (
                    current_position.x < 0
                    or current_position.y < 0
                    or current_position.x > 1920
                    or current_position.y > 1080
                ):
                    pyautogui.moveTo(960, 540, duration=0.5)
                    current_position = pyautogui.position()

            print(current_position)
            last_position = current_position

            threading.Timer(3, shake_mouse).start()
        else:
            last_position = current_position
            # Restart the timer
            threading.Timer(interval, check_mouse_movement).start()
        # print("Stop Shaking","current time:",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Start the first timer
    threading.Timer(interval, check_mouse_movement).start()


def translate_promot_C():
    lock = threading.Lock()
    time1 = datetime.now()

    lock1 = threading.Lock()
    should_print = False
    should_print_E = False

    def on_activate(key):
        nonlocal should_print
        nonlocal should_print_E
        print(key)
        if COMBINATION == key:
            lock1.acquire()
            should_print_E = False
            should_print = True
            lock1.release()
        elif COMBINATION_E == key:
            print("E")
            lock1.acquire()
            should_print = False
            should_print_E = True
            lock1.release()
        elif COMBINATION_P == key:
            lock1.acquire()
            # 调用脚本运行 python3 pic.py
            subprocess.run(["python3", "pic.py"])
            lock1.release()
        

    # The key combination to check
    COMBINATION = {
        keyboard.Key.cmd,
        keyboard.Key.shift,
        keyboard.KeyCode.from_char("p"),
    }  # Use cmd for Mac

    COMBINATION_E = {
        keyboard.Key.cmd,
        keyboard.Key.shift,
        keyboard.KeyCode.from_char("o"),
    }  # Use cmd for Mac

    COMBINATION_P = {
        keyboard.Key.ctrl,
        keyboard.KeyCode.from_char("p"),
    }  # Use cmd for Mac

    # The currently active modifiers
    current_keys = set()

    def on_press(key):
        if key in COMBINATION or key in COMBINATION_E or key in COMBINATION_P:
            current_keys.add(key)

            if COMBINATION.issubset(current_keys) or COMBINATION_E.issubset(
                current_keys
            ) or COMBINATION_P.issubset(current_keys):
                on_activate(current_keys)

    def on_release(key):
        nonlocal should_print_E
        nonlocal should_print
        nonlocal time1
        min_time_interval_sec = 0.3
        try:
            current_keys.remove(key)
            if key == keyboard.Key.cmd:
                lock1.acquire()
                if should_print:
                    should_print = False
                    lock1.release()

                    lock.acquire()
                    if (datetime.now() - time1).seconds < min_time_interval_sec:
                        lock.release()
                        return
                    time1 = datetime.now()
                    # The text to be input
                    text = "Translate into Chinese with computer science paper terminology. Only output translation results"
                    sleep(0.02)
                    for i in range(0, len(text)):
                        kb.write(text[i])
                        sleep(0.01)
                    kb.press_and_release("enter")
                    lock.release()
                elif should_print_E:
                    should_print_E = False
                    lock1.release()

                    lock.acquire()
                    if (datetime.now() - time1).seconds < min_time_interval_sec:
                        lock.release()
                        return
                    time1 = datetime.now()
                    # The text to be input
                    text = "Translate into English with computer science paper terminology. Only output translation results"
                    sleep(0.02)
                    for i in range(0, len(text)):
                        kb.write(text[i])
                        sleep(0.01)
                    kb.press_and_release("enter")
                    lock.release()
                else:
                    lock1.release()
        except KeyError:
            pass  # Deal with a key like shift being released

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    threading.Thread(target=translate_promot_C).start()
    threading.Thread(target=mo).start()
