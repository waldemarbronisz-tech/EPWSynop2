from PySide6.QtCore import QPointF
from epwsynoptic.graphics.routing import route_orthogonal

def test_straight_routing():
    p1 = QPointF(0, 0)
    p2 = QPointF(100, 0)
    route = route_orthogonal(p1, p2)
    assert len(route) == 2
    assert route[0] == p1
    assert route[1] == p2

def test_elbow_routing():
    p1 = QPointF(0, 0)
    p2 = QPointF(100, 100)
    route = route_orthogonal(p1, p2)
    # Should create an elbow: (0,0) -> (50,0) -> (50,100) -> (100,100)
    assert len(route) == 4
    assert route[0] == p1
    assert route[1] == QPointF(50, 0)
    assert route[2] == QPointF(50, 100)
    assert route[3] == p2
