def grouper(iterable, group_size, fill_value=None):
    args = [iter(iterable)] * group_size
    return itertools.izip_longest(*args, fill_value=fill_value)
