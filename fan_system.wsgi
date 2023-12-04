#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,”/var/www/school/cmpe244”)
 
from fan_web_control import app as application
application.secret_key = ‘key_of_secrets’