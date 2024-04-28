class Math:
    @staticmethod
    def get_perpendicular_point(start_pos: tuple, end_pos: tuple):
        # Calculate midpoint
        mid_point = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
        # Calculate vector from start to end
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        # Rotate vector by 90 degrees
        perpendicular_dx = -dy
        perpendicular_dy = dx
        # Add perpendicular vector to midpoint
        control_point = (
            mid_point[0] + (perpendicular_dx // 2),
            mid_point[1] + (perpendicular_dy // 2),
        )
        return control_point

    @staticmethod
    def bezier_curve(
        start_pos: tuple,
        end_pos: tuple,
        t: float,
        control_point: tuple = (0, 0),
    ):
        if control_point == (0, 0):
            control_point = Math.get_perpendicular_point(start_pos, end_pos)
        x = (
            (1 - t) ** 2 * start_pos[0]
            + 2 * (1 - t) * t * control_point[0]
            + t**2 * end_pos[0]
        )
        y = (
            (1 - t) ** 2 * start_pos[1]
            + 2 * (1 - t) * t * control_point[1]
            + t**2 * end_pos[1]
        )
        return int(x), int(y)
