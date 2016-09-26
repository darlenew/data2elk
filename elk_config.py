#!/usr/bin/env python
"""ELK(Elasticsearch-Logstash-Kibana)"""

import os
import sys
import subprocess
from commands import *

def ConfigElk(ip):
    """ Check configuration For Java & ELK components on Linux VM
        
        @ip: IP address for Kibana & ElasticSearch Instance.
    """
    jcheck   =  getoutput('java -version')
    escheck  = getoutput('/etc/init.d/elasticsearch status')
    kicheck  = getoutput('/etc/init.d/kibana status')
    logcheck = getoutput('/etc/init.d/logstash status')
    if not "Java(TM) SE Runtime Environment" in jcheck:
       JavaUpdateCheck()
    if not "elasticsearch is running" in escheck:
       ElasticSearchInstall(ip)
    if not "kibana is running" in kicheck:
       KibanaInstall(ip)
    if not "logstash is running" in logcheck:
       LogstashInstall(ip)


def JavaUpdateCheck():
    """ Configure the required Java Version on the host """

    java_cmd = "sudo add-apt-repository -y ppa:webupd8team/java ; sudo apt-get update ; sudo apt-get -y install oracle-java8-installer"
    task  = subprocess.Popen(java_cmd, shell=True, stderr=subprocess.PIPE)
    print task
    while True:
          out = task.stderr.read(1)
          if out == '' and task.poll() != None:
             break
          if out != '':
             sys.stdout.write(out)
             sys.stdout.flush()
     
   

def ElasticSearchInstall(ip):
    """ Install & Configure ElasticSearch on host

        @ip: IP address for Kibana & ElasticSearch Instance.
    """
    elastic_search_cmd = 'wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -;echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list;sudo apt-get update;sudo apt-get -y install elasticsearch;sudo sed -i.bak "s/.*network.*host.*/network\.host: \"%s\"/g" /etc/elasticsearch/elasticsearch.yml;sudo service elasticsearch restart;sudo update-rc.d elasticsearch defaults 95 10'% ip
 
    task  = subprocess.Popen(elastic_search_cmd, shell=True, stderr=subprocess.PIPE)
    print task
    while True:
          out = task.stderr.read(1)
          if out == '' and task.poll() != None:
             break
          if out != '':
             sys.stdout.write(out)
             sys.stdout.flush()
    

def KibanaInstall(ip):
    """ Install & Configure Kibana on host

        @ip: IP address for Kibana & ElasticSearch Instance.
    """

    kibana_cmd = 'echo "deb http://packages.elastic.co/kibana/4.4/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.4.x.list;sudo apt-get update;sudo apt-get -y install kibana;sudo sed -i.bak "s/.*server\.host:.*/server\.host: \"%s\"/g" /opt/kibana/config/kibana.yml;sudo sed -i.bak "s/^# elasticsearch\.url/elasticsearch\.url/g" /opt/kibana/config/kibana.yml;sudo update-rc.d kibana defaults 96 9;sudo service kibana start'% ip

    task  = subprocess.Popen(kibana_cmd, shell=True, stderr=subprocess.PIPE)
    print task
    while True:
          out = task.stderr.read(1)
          if out == '' and task.poll() != None:
             break
          if out != '':
             sys.stdout.write(out)
             sys.stdout.flush()

def LogstashInstall(ip):
    """ Install & Configure Logstash on host

        @ip: IP address for Kibana & ElasticSearch Instance.
    """

    logstash_cmd = "echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list;sudo apt-get update;sudo apt-get install logstash"
    task  = subprocess.Popen(logstash_cmd, shell=True, stderr=subprocess.PIPE)
    print task
    while True:
          out = task.stderr.read(1)
          if out == '' and task.poll() != None:
             break
          if out != '':
             sys.stdout.write(out)
             sys.stdout.flush()
if __name__ == "__main__":
    ip = sys.argv[0]
    if len(sys.argv) > 1:
       ip = sys.argv[1]
    else:
       ip = 'localhost'
    ConfigElk(ip)
