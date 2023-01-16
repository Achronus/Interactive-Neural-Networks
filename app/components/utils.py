

def hex_to_rgba(hexcode: str, transparency: float = 1) -> tuple:
    """
    Converts a string hex code colour into a rgba tuple.

    :param hexcode: (str) a hexcode colour in string format appended with a '#'
    :param transparency: (float) transparency value for the alpha in 'rgba'. Defaults to 1 (no transparency)

    :return: a tuple of float values. For example, hex_to_rgba('#5BAFF7', 1) -> (91, 175, 247, 1)
    """
    rgba = [int(hexcode.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    rgba.append(transparency)
    return tuple(rgba)
