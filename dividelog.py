with open('log2018_12_03_10_14_19.txt') as myfile:
    index = 0
    while True:
        index += 1
        try:
            with open('log2018_12_03_10_14_19_part_%03d.txt' % index, 'w') as f:
                for _ in xrange(100000):
                    f.write(myfile.next())
        except StopIteration:
            break
