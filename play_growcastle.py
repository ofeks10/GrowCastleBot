from win32api import GetSystemMetrics
import win32gui
from python_imagesearch.imagesearch import imagesearch_region_loop, imagesearcharea, click_image
import argparse
import time
import threading


def parse_args():
    parser = argparse.ArgumentParser(description='This script will automate level advancements for grow castle')
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


is_in_menu = True


def search_for_replay(start_x, start_y, end_x, end_y):
    global is_in_menu
    print('thread started')
    print(start_x, start_y, end_x, end_y)
    while not is_in_menu:
        pos = imagesearcharea('./references/Replay.png', start_x, start_y, end_x, end_y)
        if pos[0] != -1:
            is_in_menu = True
        time.sleep(1)


def main():
    global is_in_menu
    args = parse_args()
    start_x, start_y = 0, 0
    end_x, end_y = GetSystemMetrics(0), GetSystemMetrics(1)
    if args.scrcpy_window_name:
        start_x, start_y, end_x, end_y = get_phone_window_location(args.scrcpy_window_name)

    print(start_x, start_y, end_x, end_y)

    while True:
        # Click The Replay
        pos = imagesearcharea('./references/Replay.png', start_x, start_y, end_x, end_y)
        if pos[0] == -1:
            time.sleep(.1)
            continue
        position_for_window = [0, 0]
        position_for_window[0] = pos[0] + start_x
        position_for_window[1] = pos[1] + start_y
        click_image('./references/Replay.png', position_for_window, 'left', .2, offset=7)

        # Let the animation finish
        time.sleep(.7)

        # Click the Anti-Bot press
        pos = imagesearcharea('./references/100_gems.png', start_x, start_y, end_x, end_y)
        position_for_window = [0, 0]
        position_for_window[0] = pos[0] + start_x
        position_for_window[1] = pos[1] + start_y
        print(position_for_window)
        click_image('./references/100_gems.png', position_for_window, 'left', .2, offset=7)

        is_in_menu = False
        search_thread = threading.Thread(target=search_for_replay, kwargs={
            'start_x': start_x,
            'start_y': start_y,
            'end_x': end_x,
            'end_y': end_y
        })
        search_thread.start()

        # Search for Tounge Chest
        while not is_in_menu:
            pos = imagesearcharea('./references/tongue_chest.png', start_x, start_y, end_x, end_y)
            if pos[0] != -1:
                position_for_window = [0, 0]
                position_for_window[0] = pos[0] + start_x
                position_for_window[1] = pos[1] + start_y
                print(position_for_window)
                click_image('./references/100_gems.png', position_for_window, 'left', .2, offset=7)
            time.sleep(.1)
        search_thread.join()
        print('finished one level, replaying')


if __name__ == "__main__":
    main()
