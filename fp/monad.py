[
    y
    for x in get_x(1)
    for y in get_y(x)
]


class Option(object):
    pass

Option(
    y
    for x in get_x(1)
    for y in get_y(x)
)

# for x in get_x(1):
#     for y in get_y(x):
#         y
