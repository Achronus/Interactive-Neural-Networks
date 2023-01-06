

def hex_to_rgba(hexcode: str, transparency: float = 1) -> tuple:
    """Converts a string colour hexcode into a rgba tuple."""
    rgba = [int(hexcode.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    rgba.append(transparency)
    return tuple(rgba)
