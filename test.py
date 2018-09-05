def hammingDistance(x, y):
    """
    :type x: int
    :type y: int
    :rtype: int
    """


    x_bits = []
    y_bits = []
    while x > 0 or y > 0:
        rem1 = x % 2
        x_bits.append(rem1)
        rem2 = y % 2
        y_bits.append(rem2)
        x = x // 2
        y = y // 2


    diff = 0
    for i in range(len(x_bits)):
        if x_bits[i] != y_bits[i]:
            diff += 1

hammingDistance(1,4)