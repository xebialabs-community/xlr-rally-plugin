#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import ast
import os
from pyral import Rally
from xlrelease.CredentialsFallback import CredentialsFallback
from java.net import URI


class RallyClient(object):
    def __init__(self, rally_server, username, password, oauth_key):
        print "Initializing RallyClient\n"
        self.rally_server = rally_server
        rally_url = self.rally_server['url']
        credentials = CredentialsFallback(self.rally_server, username, password).getCredentials()
        self.rest_api = None
        self.configure_proxy()
        self.rest_api = Rally(URI(rally_url), credentials['username'], credentials['password'],
                              apikey=oauth_key if oauth_key else self.rally_server['oAuthKey'], verify_ssl_cert=False)

    @staticmethod
    def create_client(rally_server, username, password, oauth_key):
        print "Executing create_client() in RallyClient class in RallyClient.py\n"
        return RallyClient(rally_server, username, password, oauth_key)

    def configure_proxy(self):
        if self.rally_server['proxyHost']:
            if self.rally_server['proxyUsername']:
                os.environ["HTTP_PROXY"] = "http://%s:%s@%s:%s" % (
                    self.rally_server['proxyUsername'], self.rally_server['proxyPassword'],
                    self.rally_server['proxyHost'],
                    self.rally_server['proxyPort'])
                os.environ["HTTPS_PROXY"] = "https://%s:%s@%s:%s" % (
                    self.rally_server['proxyUsername'], self.rally_server['proxyPassword'],
                    self.rally_server['proxyHost'],
                    self.rally_server['proxyPort'])
            os.environ["HTTP_PROXY"] = "http://%s:%s" % (self.rally_server['proxyHost'], self.rally_server['proxyPort'])
            os.environ["HTTPS_PROXY"] = "https://%s:%s" % (
                self.rally_server['proxyHost'], self.rally_server['proxyPort'])

    def lookup_item_by_formatted_id(self, type, formatted_id):
        response = self.rest_api.get(type, fetch="ObjectID", query="FormattedID = %s" % formatted_id)

        if not response.errors:
            print("Total results: %d\n" % response.resultCount)
            result = response.next()
            return result.ObjectID
        else:
            print("The following errors occurred: ")
            for err in response.errors:
                print("\t" + err)
            return None

    def create_item(self, workspace, project, properties, user_story_formatted_id, user_story_type, property_type,
                    item_type):
        self.rest_api.setWorkspace(workspace)
        self.rest_api.setProject(project)
        story_ref = self.lookup_item_by_formatted_id(user_story_type, user_story_formatted_id)

        property_dict = dict(ast.literal_eval(properties))
        property_dict[property_type] = story_ref

        item_create_response = self.rest_api.put(item_type, property_dict)

        print "Executed successful on Rally"
        return item_create_response.FormattedID

    def update_item(self, workspace, project, properties, item_formatted_id, item_type):
        self.rest_api.setWorkspace(workspace)
        self.rest_api.setProject(project)
        item_object_id = self.lookup_item_by_formatted_id(item_type, item_formatted_id)
        property_dict = dict(ast.literal_eval(properties))
        property_dict["ObjectID"] = item_object_id

        update_response = self.rest_api.post(item_type, property_dict)

        print "Executed successful on Rally"
        return update_response.FormattedID
