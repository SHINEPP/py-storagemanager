def byte2string(size: int) -> str:
    """
    字节大小转字符串
    :param size:
    :return:
    """
    value = size
    if value < 1024:
        return f'{value}B'

    value = value / 1024
    if value < 1024:
        return f'{round(value, 1)}KB'

    value = value / 1024
    if value < 1024:
        return f'{round(value, 1)}MB'

    value = value / 1024
    if value < 1024:
        return f'{round(value, 1)}GB'

    value = value / 1024
    return f'{round(value, 1)}TB'
