from lib.utils.math import Math


def test_bezier_curve():
    assert Math.bezier_curve((5, 5), (10, 10), 0.5) == (6, 8)
    assert Math.bezier_curve((5, 10), (10, 5), 0.5) == (8, 8)
    assert Math.bezier_curve((10, 10), (5, 5), 0.5) == (8, 6)
    assert Math.bezier_curve((10, 5), (5, 10), 0.5) == (6, 6)
