import pcap_statistic as ps
import pcap_statistic_single as ps_s
import pcap_analyzer as pa
ARGS = None

def pcap_main():
    if ARGS.single == 't':
        ps_s.main(ARGS.pcappath, ARGS.csvpath, 
                  ARGS.appname, ARGS.experiment_count)
    else:    
        ps.main(ARGS.pcappath, ARGS.csvpath)



def pcap_main_single(pcappath, csvpath, appname, excount):
        ps_s.main(pcappath, csvpath, 
                  appname, excount)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="packet analyzer")
    parser.add_argument('--csvpath', '-c',
                        required=False,
                        help='input csvpath')
    parser.add_argument('--imgpath', '-i',
                        required=False,
                        help='input imgpath')
    parser.add_argument('--pcappath', '-p',
                        required=True,
                        help='input pcappath')
    parser.add_argument('--single', '-s',
                        default='f',
                        help='input single result[t or f]')
    parser.add_argument('--experiment-count', '-e',
                        type=int,
                        required=False,
                        help='input experiment count[only single=t]')
    parser.add_argument('--appname', '-a',
                        required=False,
                        help='input package name [only single=t]')
    ARGS = parser.parse_args()
        
    pcap_main()
