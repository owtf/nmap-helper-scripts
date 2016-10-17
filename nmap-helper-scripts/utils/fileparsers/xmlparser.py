from libnmap.parser import NmapParser, NmapParserException
from libnmap.objects.service import NmapService
from collections import defaultdict

###########################################################
# <<<<< TO-D0 >>>>>>>>
# 1. Write Custom Exceptions
# 2. Add support for all types of file inputs
# 3. Enhance output readability using colors.
# #########################################################


def _stats(report):
    ''' Prints statistics about the scan '''
    if not report:
        print "[!] Nothing to parse. Exiting"
        exit(1)

    # Check for inconsistency in the reports.
    if not report.is_consistent():
        print "[!] Inconsistent Report. Actual results might be incomplete."
    print "\n", report.summary

    # Print the list of hosts that are up and get services.
    print "\nThe following hosts are up (%d of %d): \n" % (report.hosts_up, report.hosts_total)
    for host in report.hosts:
        if host.is_up():
            print "* %s with %d open ports\t(%s)" % (host.address, len(host.get_open_ports()), host.hostnames[0])


def parse_xml(filepath):
    '''Parses an XML file and finds information about the hosts and returns the scan object'''

    try:
        nmap_report = NmapParser.parse_fromfile(filepath)
    except TypeError:
        print "[!] IOError : Cannot read from the file. Try again."
        return 0
        sys.exit()
    except NmapParserException:
        print "[!] Bad XML file. The scan was probably interrupted."
        return 0

    _stats(nmap_report)
    return nmap_report


def map_http_ports(report):
    '''Maps hostname to the list of open ports available'''
    portmap = defaultdict(list)
    for host in report.hosts:
        for attr in host.services:
            if attr.get_dict()['service'] in ['http', 'https']:
                portmap[host.hostnames[0]].append((attr.get_dict()['port'], attr.get_dict()['service']))
    return dict(portmap)
