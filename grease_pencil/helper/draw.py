import math


def draw_line(gp_frame, p0: tuple, p1: tuple, width=0):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = "3DSPACE"  # Allows for editing
    gp_stroke.line_width = width

    gp_stroke.points.add(count=2)
    gp_stroke.points[0].co = (p0[0], 0, p0[1])
    gp_stroke.points[1].co = (p1[0], 0, p1[1])
    return gp_stroke


def draw_circle(gp_frame, center: tuple, radius: float, segments: int):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = "3DSPACE"  # Allows for editing
    gp_stroke.draw_cyclic = True

    angle = 2 * math.pi / segments
    gp_stroke.points.add(count=segments)
    for i in range(segments):
        x = center[0] + radius * math.cos(angle * i)
        y = center[1] + radius * math.sin(angle * i)
        z = center[2]
        gp_stroke.points[i].co = (x, y, z)

    return gp_stroke
