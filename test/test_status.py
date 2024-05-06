import time

from lib.utils.status import Status


def test_is_paused():
    assert Status.is_paused() is True


def test_get_status_paused():
    assert Status.get_status() == "PAUSED"


def test_resume():
    Status.resume()
    assert Status.is_paused() is False
    assert Status.get_status() == "RUNNING"


def test_pause():
    Status.pause()
    assert Status.is_paused() is True
    assert Status.get_status() == "PAUSED"


def test_is_sleeping():
    assert Status.is_sleeping() is False


def test_sleep():
    start_time = time.time()
    Status.sleep(1)
    end_time = time.time()
    assert end_time - start_time >= 1
