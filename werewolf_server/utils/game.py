def circular_access(lst, start_index):
    length = len(lst)
    if length == 0:
        return []

    for i in range(length):
        yield lst[(start_index + i) % length]