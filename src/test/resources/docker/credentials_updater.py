#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# Create directories
import sys
import json
import base64
import urllib
import urllib.parse
import urllib.request
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

print("Updating credentials")

xlr_username="admin"
xlr_password="admin"
base64string = base64.encodestring(('%s:%s' % (xlr_username, xlr_password)).encode()).decode().replace('\n', '')

def get_configuration_object(server_title, server_type):
    url_encoded_title = urllib.parse.quote(server_title)
    url = "http://xlr:5516/api/v1/config/byTypeAndTitle?configurationType=%s&title=%s" % (server_type, url_encoded_title)
    request = urllib.request.Request(url)
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib.request.urlopen(request)
    return json.loads(result.read())[0]

def save_configuration_object(config_object):
    headers = {'Content-Type': 'application/json'}
    request = urllib.request.Request("http://xlr:5516/api/v1/config/", json.dumps(config_object).encode("utf-8"), headers)
    request.add_header("Authorization", "Basic %s" % base64string)
    request.get_method = lambda: 'POST'
    result2 = urllib.request.urlopen(request)

def update_ci(server_title, server_type, username, properties):
    print("Processing credential [%s] for server type [%s] with title [%s]" % (username, server_type, server_title))
    config_object = {}
    try:
        config_object = get_configuration_object(section, server_type)
    except:
        print("Could not find existing config object for title %s" % server_title)

    config_object["title"] = server_title
    for item in properties:
        config_object[item[0]] = item[1]
    save_configuration_object(config_object)

cp = RawConfigParser()
#To avoid parser to convert all keys to lowercase by default
cp.optionxform = str
cp.read(sys.argv[1])

for section in cp.sections():
    update_ci(section, cp.get(section, "type"), cp.get(section, "username"), cp.items(section))

print("Updated credentials")
