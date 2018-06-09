#!/usr/bin/env python
"""ELK(Elasticsearch-Logstash-Kibana)"""

import os
import sys
import subprocess
from commands import *


def execute(cmd):
    """Execute shell command"""
    task  = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    sys.stdout.write(cmd + '\n')
    while True:
          out = task.stderr.read(1)
          if out == '' and task.poll() != None:
             break
          if out != '':
             sys.stdout.write(out)
             sys.stdout.flush()


def ConfigElk(ip):
    """ Check configuration For Java & ELK components on Linux VM
        
        @ip: IP address for Kibana & ElasticSearch Instance.
    """
    jcheck   =  getoutput('java -version')
    escheck  = getoutput('/etc/init.d/elasticsearch status')
    kicheck  = getoutput('/etc/init.d/kibana status')
    logcheck = os.path.exists("/etc/init.d/logstash")
    if not "Java(TM) SE Runtime Environment" in jcheck:
       JavaUpdateCheck()

    # install public signing key
    execute("wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -")
    execute("sudo apt-get install apt-transport-https")
    execute("echo \"deb https://artifacts.elastic.co/packages/6.x/apt stable main\" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list")

    if not "elasticsearch is running" in escheck:
       ElasticSearchInstall(ip)
    if not "kibana is running" in kicheck:
       KibanaInstall(ip)
    if logcheck == False:
       LogstashInstall(ip)


def ubuntu_install(package):
    sys.stdout.write("installing {}\n".format(package))
    cmd = 'sudo apt-get update;sudo apt-get -y install {package}'.format(package=package)
    execute(cmd)


def JavaUpdateCheck():
    """ Configure the required Java Version on the host """

    java_cmd = "sudo add-apt-repository -y ppa:webupd8team/java ; sudo apt-get update ; sudo apt-get -y install oracle-java8-installer"
    execute(java_cmd)
   

def ElasticSearchInstall(ip):
    """ Install & Configure ElasticSearch on host

        @ip: IP address for Kibana & ElasticSearch Instance.
    """
    ubuntu_install('elasticsearch')
    elastic_search_cmd = 'sudo sed -i.bak "s/.*network.*host.*/network\.host: \"%s\"/g" /etc/elasticsearch/elasticsearch.yml;sudo service elasticsearch restart;sudo update-rc.d elasticsearch defaults 95 10'% ip
    execute(elastic_search_cmd)
    

def KibanaInstall(ip):
    """ Install & Configure Kibana on host

        @ip: IP address for Kibana & ElasticSearch Instance.
    """
    ubuntu_install('kibana')
    kibana_cmd = 'sudo sed -i.bak "s/.*server\.host:.*/server\.host: \"%s\"/g" /opt/kibana/config/kibana.yml;sudo sed -i.bak "s/^# elasticsearch\.url/elasticsearch\.url/g" /opt/kibana/config/kibana.yml;sudo update-rc.d kibana defaults 96 9;sudo service kibana start'% ip
    execute(kibana_cmd)
 

def LogstashInstall(ip):
    """ Install & Configure Logstash on host

        @ip: IP address for Kibana & ElasticSearch Instance.
    """
    ubuntu_install('logstash')


if __name__ == "__main__":
    ip = sys.argv[0]
    if len(sys.argv) > 1:
       ip = sys.argv[1]
    else:
       ip = 'localhost'
    ConfigElk(ip)
