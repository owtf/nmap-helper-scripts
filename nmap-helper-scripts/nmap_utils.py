import argparse
from utils.fileparsers.xmlparser import parse_xml, map_http_ports
from utils.owtf.owtf_api import addtarget


def init_args():
    '''Initializes argparser and returns the parser object'''

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file", required=True)
    parser.add_argument('--owtf', '-O', action="store_true", help="Feed all http/https interfaces found to OWTF")
    args = parser.parse_args()
    return args


def main():
        args = init_args()
        report = parse_xml(args.input)
        if args.owtf:
            portmap = map_http_ports(report)
            addtarget(portmap)


if __name__ == '__main__':
    main()
