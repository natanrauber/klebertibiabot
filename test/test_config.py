from lib.config import Config


# OT Server
def test_get_OTServer():
    assert Config.getOTServer() is False


def test_set_OTServer():
    Config.setOTServer(True)
    assert Config.getOTServer() is True


# Attack
def test_get_attack():
    assert Config.getAttack() is False


def test_set_attack():
    Config.setAttack(True)
    assert Config.getAttack() is True


# Heal
def test_get_heal():
    assert Config.getHeal() is False


def test_set_heal():
    Config.setHeal(True)
    assert Config.getHeal() is True


# Loot
def test_get_loot():
    assert Config.getLoot() is False


def test_set_loot():
    Config.setLoot(True)
    assert Config.getLoot() is True


def test_get_screen_center_x():
    assert Config.getScreenCenterX() == 0


def test_get_screen_center_y():
    assert Config.getScreenCenterY() == 0


def test_set_screen_center():
    Config.setScreenCenter(x=100, y=200)
    assert Config.getScreenCenterX() == 100
    assert Config.getScreenCenterY() == 200


def test_get_SQM_size():
    assert Config.getSqmSize() == 0


def test_set_SQM_size():
    Config.setSqmSize(40)
    assert Config.getSqmSize() == 40


# Walk
def test_get_walk():
    assert Config.getWalk() is False


def test_set_walk():
    Config.setWalk(True)
    assert Config.getWalk() is True


# Eat
def test_get_eat():
    assert Config.getEat() is False


def test_set_eat():
    Config.setEat(True)
    assert Config.getEat() is True


# Drop
def test_get_drop():
    assert Config.getDrop() is False


def test_set_drop():
    Config.setDrop(True)
    assert Config.getDrop() is True
