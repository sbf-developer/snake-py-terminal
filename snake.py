#!/usr/bin/env python3
"""Terminal Snake — no extra packages needed on Windows."""

import random
import shutil
import sys
import time
from collections import deque

DIRS = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
OPPOSITE = {"w": "s", "s": "w", "a": "d", "d": "a"}


def random_food(height, width, snake):
    occupied = set(snake)
    while True:
        pos = (random.randint(1, height - 2), random.randint(1, width - 2))
        if pos not in occupied:
            return pos


def enable_ansi():
    if sys.platform != "win32":
        return
    try:
        import ctypes
        stdout = ctypes.windll.kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        ctypes.windll.kernel32.GetConsoleMode(stdout, ctypes.byref(mode))
        ctypes.windll.kernel32.SetConsoleMode(stdout, mode.value | 4)
    except Exception:
        pass


def play():
    import msvcrt

    out = sys.stdout.write
    flush = sys.stdout.flush
    arrows = {72: "w", 80: "s", 75: "a", 77: "d"}

    def read_key():
        while msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b"\x00", b"\xe0"):
                code = msvcrt.getch()[0]
                if code in arrows:
                    return arrows[code]
                continue
            try:
                return key.decode().lower()
            except UnicodeDecodeError:
                continue
        return None

    def enter_screen():
        out("\033[?1049h\033[?25l")
        flush()

    def leave_screen():
        out("\033[?1049l\033[?25h")
        flush()

    def put(y, x, ch):
        out(f"\033[{y + 2};{x + 1}H{ch}")

    def hud(score):
        out(f"\033[1;1H Score: {score}   WASD / arrows to move   q to quit\033[K")

    def draw_border(height, width):
        grid = [[" "] * width for _ in range(height)]
        for r in range(height):
            grid[r][0] = grid[r][width - 1] = "|"
        for c in range(width):
            grid[0][c] = grid[height - 1][c] = "-"
        for y, x in ((0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)):
            grid[y][x] = "+"
        out("\033[1;1H Score: 0   WASD / arrows to move   q to quit\n")
        out("\n".join("".join(row) for row in grid))
        flush()

    enable_ansi()
    term_h, term_w = shutil.get_terminal_size((24, 80))
    height = min(max(term_h - 3, 15), 20)
    width = min(max(term_w - 4, 40), 56)

    enter_screen()
    draw_border(height, width)

    snake = deque([(height // 2, width // 2)])
    direction = "d"
    food = random_food(height, width, snake)
    score = 0
    pending = None

    for sy, sx in snake:
        put(sy, sx, "#")
    put(food[0], food[1], "*")
    flush()

    try:
        while True:
            key = read_key() or pending
            pending = None
            if key == "q":
                return
            if key in DIRS and key != OPPOSITE[direction]:
                direction = key

            dy, dx = DIRS[direction]
            y, x = snake[0]
            head = (y + dy, x + dx)

            if not (0 < head[0] < height - 1 and 0 < head[1] < width - 1) or head in snake:
                break

            tail = snake[-1]
            snake.appendleft(head)
            put(head[0], head[1], "#")
            if head == food:
                score += 1
                food = random_food(height, width, snake)
                put(food[0], food[1], "*")
            else:
                snake.pop()
                put(tail[0], tail[1], " ")

            hud(score)
            flush()

            deadline = time.monotonic() + 0.12
            while time.monotonic() < deadline:
                key = read_key()
                if key == "q":
                    return
                if key in DIRS and key != OPPOSITE[direction]:
                    pending = key
                    break
                time.sleep(0.01)

        print(f"GAME OVER — score: {score}")
        print("Press any key to exit...")
        msvcrt.getch()
    finally:
        leave_screen()


if __name__ == "__main__":
    if sys.platform == "win32":
        play()
    else:
        import curses

        def play_curses(stdscr):
            curses.curs_set(0)
            stdscr.nodelay(True)
            stdscr.timeout(120)
            height, width = stdscr.getmaxyx()
            snake = deque([(height // 2, width // 2)])
            direction = curses.KEY_RIGHT
            deltas = {
                curses.KEY_UP: (-1, 0),
                curses.KEY_DOWN: (1, 0),
                curses.KEY_LEFT: (0, -1),
                curses.KEY_RIGHT: (0, 1),
            }
            opp = {curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP,
                   curses.KEY_LEFT: curses.KEY_RIGHT, curses.KEY_RIGHT: curses.KEY_LEFT}
            food = random_food(height, width, snake)
            score = 0
            while True:
                key = stdscr.getch()
                if key in deltas and key != opp[direction]:
                    direction = key
                dy, dx = deltas[direction]
                head = (snake[0][0] + dy, snake[0][1] + dx)
                if not (0 < head[0] < height - 1 and 0 < head[1] < width - 1) or head in snake:
                    break
                snake.appendleft(head)
                if head == food:
                    score += 1
                    food = random_food(height, width, snake)
                else:
                    snake.pop()
                stdscr.erase()
                stdscr.border()
                stdscr.addstr(0, 2, f" Score: {score} ")
                stdscr.addstr(food[0], food[1], "*")
                for y, x in snake:
                    stdscr.addstr(y, x, "#")
                stdscr.refresh()
            stdscr.addstr(height // 2, max(0, width // 2 - 6), "GAME OVER")
            stdscr.getch()

        curses.wrapper(play_curses)
