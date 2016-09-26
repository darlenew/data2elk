#!/usr/bin/env python
"""data2elk.py feeds csv data into Elasticsearch-Logstash-Kibana"""

import os
import sys
import csv
from elk_config import ConfigElk as config_elk

CONFIG_TEMPLATE = """# logstash config, generated by data2elk.py
input {
  file {
    path => "%s"
    type => "csv"
    start_position => "beginning"
  }
}
 
filter { 
  csv {
     columns => %s
     separator => "%s"
  } 
}
 
output {
  elasticsearch { 
    action => "index"
    hosts => "localhost" 
    index => "logstash-%%{+YYYY.MM.dd}"
    workers => 1
  }
  stdout { codec => rubydebug }
}
"""

def get_columns(path, delimiter=',', quotechar='"'):
    """Extract column names from the CSV

    @param path: path to CSV file
    @param delimiter: CSV delimiter character
    @param quotechar: character used to quote fields in CSV
    @return: list of column names
    """
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        header = reader.next()  

    return header


def generate_config(config_path, csv_path, columns, delimiter=',', quotechar='"'):
    """Generate Logstash config file.

    @param config_path: path to write Logstash config to.
    @param csv_path: path to csv input data
    @param columns: column names in the csv
    @param delimiter: CSV delimiter character
    @param quotechar: character used to quote fields in CSV
    @return: None
    """
    config_dir = os.path.dirname(config_path)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    data = CONFIG_TEMPLATE % (os.path.abspath(csv_path), columns, delimiter)
    with open(config_path, 'w') as fd:
        fd.write(data)


def which(program, all=False):
    """Locates the program in the directories specified by the PATH environment variable.

    @param program: the program to locate
    @param all: boolean, specify True to find all instances of the program found, 
                otherwise just the first is returned.
    @return: The path found, or None.  If all is True, returns list of all paths found.
    """              
    found = []
    for path in os.getenv("PATH").split(os.path.pathsep):
        full_path = os.path.join(path, program)
        if os.path.exists(full_path):
            if all:
                found.append(full_path)
            else:
                return full_path

    if all:
        return found


if __name__ == "__main__":
    import argparse
    import subprocess


    DEFAULT_CONFIG_PATH = '/etc/logstash/conf.d/logstash.conf'

    parser = argparse.ArgumentParser(description="Process data for Elasticsearch/Logstash/Kibana")
    parser.add_argument('-f', '--file', metavar='FILE', help='path to csv input')
    parser.add_argument('--no-header', dest='header', action='store_false', default=True,
                        help='no csv header, use generic column names')
    parser.add_argument('--delimiter', default=',',
                        help="""csv delimiter character, ',' by default""")
    parser.add_argument('--quotechar', default='"',
                        help="""csv quote character, '"' by default""")
    parser.add_argument('-o', '--output', metavar='FILE', default='/etc/logstash/conf.d/logstash.conf',
                        help='path to logstash config output, defaults to {}'.format(DEFAULT_CONFIG_PATH))
    parser.add_argument('-r', '--restart-logstash', action='store_true', default=False,
                        help='restart logstash with the generated config, if it is not already running as a daemon')
    parser.add_argument('-i', '--ip', default='localhost',
                        help='IP address for Kibana and ElasticSearch instance, defaults to localhost.')
    args = parser.parse_args()    

    if not args.file:
        sys.stdout.write("No data file specified\n")
        sys.exit(1)

    if not os.path.exists(args.file):
        sys.stdout.write("File does not exist: {}\n".format(args.file))
        sys.exit(1)

    if sys.platform.startswith('linux'):
        config_elk(args.ip)

    columns = []
    if args.header:
        columns = get_columns(args.file, delimiter=args.delimiter, quotechar=args.quotechar) 

    generate_config(args.output, args.file, columns, 
                    delimiter=args.delimiter, quotechar=args.quotechar)

    # get the path to logstash
    program = which('logstash')
    if not program:
        sys.stdout.write("No logstash installation found\n")
        sys.exit(1)

    # check if generated config is valid, raises CalledProcessError is raised if config is invalid.
    with open(os.devnull, 'w') as devnull_fd: # used to suppress output
        subprocess.check_call([program, "--configtest", "--config", args.output], stdout=devnull_fd)
  
    if args.restart_logstash:
        subprocess.call([program, '-f', args.output])    


