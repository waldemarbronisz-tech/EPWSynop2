from typing import List, Tuple
from PySide6.QtCore import QPointF

def route_orthogonal(start: QPointF, end: QPointF) -> List[QPointF]:
    """
    Simple orthogonal routing.
    If X or Y aligned, returns straight line.
    Otherwise, prefers one bend (elbow) or two bends (dogleg).
    """
    points = [start]

    # Check if straight line
    if abs(start.x() - end.x()) < 1.0 or abs(start.y() - end.y()) < 1.0:
        points.append(end)
        return points

    # Default to simple elbow routing for now: horizontal then vertical
    # In a full implementation, this would check bounding boxes and avoid obstacles
    mid_x = (start.x() + end.x()) / 2.0

    points.append(QPointF(mid_x, start.y()))
    points.append(QPointF(mid_x, end.y()))
    points.append(end)

    return points
