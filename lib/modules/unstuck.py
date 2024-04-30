import time

from lib.config import DESTROY_KEY, ROPE_KEY, Config
from lib.utils.keyboard import Keyboard
from lib.utils.mouse import Mouse


def stack_items():
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Mouse.drag_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() + (Config.getSqmSize() * 2),
            Config.getScreenCenterY() - (Config.getSqmSize() * 2),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() - (Config.getSqmSize() * 2),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() - (Config.getSqmSize() * 2),
            Config.getScreenCenterY() - (Config.getSqmSize() * 2),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
        (
            Config.getScreenCenterX() - (Config.getSqmSize() * 2),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() - (Config.getSqmSize() * 2),
            Config.getScreenCenterY() + (Config.getSqmSize() * 2),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() + (Config.getSqmSize() * 2),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
        (
            Config.getScreenCenterX() + (Config.getSqmSize() * 2),
            Config.getScreenCenterY() + (Config.getSqmSize() * 2),
        ),
    )
    Mouse.drag_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
        (
            Config.getScreenCenterX() + (Config.getSqmSize() * 2),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)


def destroy_items():
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    time.sleep(0.01)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
    )
    time.sleep(0.3)
    Keyboard.press(DESTROY_KEY)
    time.sleep(0.3)
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    time.sleep(0.3)
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)


def rope_all():
    Mouse.lock(True)
    _initPos = Mouse.get_pos()
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() - Config.getSqmSize(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX() - Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY() + Config.getSqmSize(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX() + Config.getSqmSize(),
            Config.getScreenCenterY(),
        ),
    )
    time.sleep(1)
    Keyboard.press(ROPE_KEY)
    Mouse.click_left(
        (
            Config.getScreenCenterX(),
            Config.getScreenCenterY(),
        ),
    )
    Mouse.set_pos(_initPos, useOffSet=False)
    Mouse.lock(False)
