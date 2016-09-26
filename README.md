# data2elk: Log Visualization for Dummies

Get up and running with the ELK stack in minutes!

 * Takes an input CSV file
 * Automatically downloads, installs, and configures ElasticSearch, Logstash, and Kibana
 * Automatically parses and indexes your data
 * Point your browser to http://127.0.0.1:5601/ and start exploring!

# Requirements

 * [python-2.7](https://www.python.org/download/releases/2.7/)

# Usage
```
usage: data2elk.py [-h] [-f FILE] [--no-header] [--delimiter DELIMITER]
                   [--quotechar QUOTECHAR] [-o FILE] [-r]

Process data for Elasticsearch/Logstash/Kibana

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path to csv input
  --no-header           no csv header, use generic column names
  --delimiter DELIMITER
                        csv delimiter character, ',' by default
  --quotechar QUOTECHAR
                        csv quote character, '"' by default
  -o FILE, --output FILE
                        path to logstash config output, defaults to
                        /etc/logstash/conf.d/logstash.conf
  -r, --restart-logstash
                        restart logstash with the generated config, if it is 
                        not already running as a daemon
  -i IP, --ip IP        IP address for Kibana and ElasticSearch instance,
                        defaults to localhost.
```



