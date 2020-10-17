from win32api import GetSystemMetrics
import win32gui
from python_imagesearch.imagesearch import imagesearch_region_loop, imagesearcharea, click_image, region_grabber
import argparse
import time
import threading
import random


is_in_menu = True


def parse_args():
    parser = argparse.ArgumentParser(description='This script will automate level advancements for grow castle')
    parser.add_argument('mode', choices=['replay', 'battle'], help='Whether to replay the same level or battle')
    parser.add_argument('--scrcpy_window_name', '-w', help='The name of the window of scrcpy.  This is for optimizations')
    return parser.parse_args()


class WindowPosition:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y


def get_phone_window_location(window_name):
    win_pos = WindowPosition(0, 0, 0, 0)
    def callback(hwnd, win_pos):
        if win32gui.GetWindowText(hwnd) == window_name:
            rect = win32gui.GetWindowRect(hwnd)
            win_pos.start_x = rect[0]
            win_pos.start_y = rect[1]
            win_pos.end_x = rect[2]
            win_pos.end_y = rect[3]

    win32gui.EnumWindows(callback, win_pos)
    if win_pos.end_x == 0 and win_pos.end_y == 0:
        raise Exception('can\'t find window')

    return (win_pos.start_x, win_pos.start_y, win_pos.end_x, win_pos.end_y)


def search_for_replay(start_x, start_y, end_x, end_y):
    global is_in_menu
    print('thread started')
    print(start_x, start_y, end_x, end_y)
    while not is_in_menu:
        pos = imagesearcharea('./references/Replay.png', start_x, start_y, end_x, end_y)
        if pos[0] != -1:
            is_in_menu = True
        time.sleep(random.randint(5, 11) / 10)


def click_image_relative_to_window(img_path, start_x, start_y, end_x, end_y, offset=7, precision=.8, im=None):
    pos = imagesearcharea(img_path, start_x, start_y, end_x, end_y, precision=precision, im=im)
    if pos[0] != -1:
        position_for_window = [0, 0]
        position_for_window[0] = pos[0] + start_x
        position_for_window[1] = pos[1] + start_y
        click_image(img_path, position_for_window, 'left', .2, offset=offset)


def start_replay(start_x, start_y, end_x, end_y):
    # Click The Replay
    pos = imagesearch_region_loop('./references/Replay.png', .1, start_x, start_y, end_x, end_y)
    position_for_window = [0, 0]
    position_for_window[0] = pos[0] + start_x
    position_for_window[1] = pos[1] + start_y
    click_image('./references/Replay.png', position_for_window, 'left', .2, offset=7)

    # Let the animation finish
    time.sleep(random.randint(7, 11) / 10)

    # Click the Anti-Bot press
    click_image_relative_to_window('./references/100_gems.png', start_x, start_y, end_x, end_y)

def start_battle(start_x, start_y, end_x, end_y):
    # Click The Battle
    pos = imagesearch_region_loop('./references/Battle.png', .1, start_x, start_y, end_x, end_y)
    position_for_window = [0, 0]
    position_for_window[0] = pos[0] + start_x
    position_for_window[1] = pos[1] + start_y
    click_image('./references/Battle.png', position_for_window, 'left', .2, offset=7)

    # Let the game start
    time.sleep(random.randint(5, 10) / 10)

    # Click the x on the wave-skip
    click_image_relative_to_window('./references/x.png', start_x, start_y, end_x, end_y)


def main():
    global is_in_menu
    args = parse_args()
    start_x, start_y = 0, 0
    end_x, end_y = GetSystemMetrics(0), GetSystemMetrics(1)
    if args.scrcpy_window_name:
        start_x, start_y, end_x, end_y = get_phone_window_location(args.scrcpy_window_name)

    menu_func = None
    if args.mode == 'battle':
        menu_func = start_battle
    elif args.mode == 'replay':
        menu_func = start_replay

    print(start_x, start_y, end_x, end_y)

    while True:
        menu_func(start_x, start_y, end_x, end_y)

        is_in_menu = False
        search_thread = threading.Thread(target=search_for_replay, kwargs={
            'start_x': start_x,
            'start_y': start_y,
            'end_x': end_x,
            'end_y': end_y
        })
        search_thread.start()

        # Search for Tounge Chest and click Alice
        while not is_in_menu:
            im = region_grabber((start_x, start_y, end_x, end_y))
            click_image_relative_to_window('./references/tongue_chest.png', start_x, start_y, end_x, end_y, im=im)
            
            # if pos[0] != -1:
            #     position_for_window = [0, 0]
            #     position_for_window[0] = pos[0] + start_x
            #     position_for_window[1] = pos[1] + start_y
            #     print('cliking chest in', position_for_window)
            #     click_image('./references/tongue_chest.png', position_for_window, 'left', .2, offset=7)

            click_image_relative_to_window('./references/Alice.png', start_x, start_y, end_x, end_y, offset=2, precision=0.92, im=im)
            time.sleep(random.randint(0, 3) / 10)
            click_image_relative_to_window('./references/Lisa.png', start_x, start_y, end_x, end_y, offset=2, precision=0.92, im=im)
            # if alice_pos[0] != -1 or lisa_pos[0] != -1:
            #     alice_position_for_window = [0, 0]
            #     alice_position_for_window[0] = alice_pos[0] + start_x
            #     alice_position_for_window[1] = alice_pos[1] + start_y
            #     lisa_position_for_window = [0, 0]
            #     lisa_position_for_window[0] = lisa_pos[0] + start_x
            #     lisa_position_for_window[1] = lisa_pos[1] + start_y
                # print('clicking witches in: ', alice_position_for_window, lisa_position_for_window)
                # if alice_pos[0]  != -1:
                #     click_image('./references/Alice.png', alice_position_for_window, 'left', .1, offset=2)
                # if lisa_pos[0] != -1:
                #     click_image('./references/Lisa.png', lisa_position_for_window, 'left', .1, offset=2)
            time.sleep(.1)
        search_thread.join()
        print('finished one level, replaying')
        is_in_menu = True


if __name__ == "__main__":
    main()
