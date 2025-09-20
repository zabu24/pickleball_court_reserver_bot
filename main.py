def print_unicode(data):
    grid_map = {}
    max_x = 0
    max_y = 0

    for x, char, y in data:
        grid_map[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    for y in range(max_y + 1):
        row = ''
        for x in range(max_x + 1):
            row += grid_map.get((x, y), ' ')
        print(row)
