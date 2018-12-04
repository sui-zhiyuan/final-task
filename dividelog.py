with open('log2018_12_04_20_17_58.txt') as myfile:
    index = 0
    while True:
        index += 1
        try:
            with open('log2018_12_04_20_17_58_part_%03d.txt' % index, 'w') as f:
                for _ in xrange(100000):
                    f.write(myfile.next())
        except StopIteration:
            break
