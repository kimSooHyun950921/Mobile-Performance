from experiments import EXP

ARGS = None
def main():
    exp = EXP(ARGS.path, ARGS.csvpath, ARGS.device, ARGS.count)
    exp.start()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AppTesting")
    parser.add_argument('--path', '-p',
                        type=str,
                        default='/home/kimsoohyun/00-Research/02-Graph/05-data/',
                        help='input default data path')
    parser.add_argument('--csvpath', '-c',
                        type=str,
                        required=True,
                        help='input app csv path')
    parser.add_argument('--device', '-d',
                        type=str,
                        required=True,
                        help='input android or ios')
    parser.add_argument('--count', '-o',
                        type=int,
                        required=True,
                        help='input count')
    ARGS = parser.parse_args()
    main()
