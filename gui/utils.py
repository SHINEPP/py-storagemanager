from PIL import Image, ImageTk


def byte2string(size: int) -> str:
    """
    字节大小转字符串
    :param size:
    :return:
    """
    value = size
    if value < 1024:
        return f'{value} B'

    value = value / 1024
    if value < 1024:
        return f'{round(value, 1)} KB'

    value = value / 1024
    if value < 1024:
        return f'{round(value, 1)} MB'

    value = value / 1024
    if value < 1024:
        return f'{round(value, 1)} GB'

    value = value / 1024
    return f'{round(value, 1)} TB'


def resize_image(path, width, height):
    image = Image.open(path)
    resized_image = image.resize((width, height))
    return ImageTk.PhotoImage(resized_image)
