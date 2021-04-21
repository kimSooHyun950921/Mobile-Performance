import csv

FLAGS = None
def main():
    with open('dataset/test.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        #for w in range(-FLAGS.width, FLAGS.width+1i):
        w = -60
        while w <= 60:
            h = -28
            #for h in range(-FLAGS.height, FLAGS.height+1):
            while h <=26:   
                writer.writerow([h, w])
                h += 6.75
            w = w + 7.5
    


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='make coordinate.csv for data')
    parser.add_argument('--width', '-w', type=int,
                        required=False,
                        help='input width')
    parser.add_argument('--height', '-t', type=int,
                        required=False,
                        help='input height')
    FLAGS = parser.parse_args()
    main()

