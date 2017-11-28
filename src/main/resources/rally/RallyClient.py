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
        if oauth_key:
            self.rest_api = Rally(URI(rally_url), apikey=oauth_key)
        else:
            self.rest_api = Rally(URI(rally_url), credentials['username'], credentials['password'])
        if self.rally_server['proxyHost']:
            self.rest_api.setProxy(URI("http://%s:%s" % (self.rally_server['proxyHost'], self.rally_server['proxyPort'])))


    @staticmethod
    def create_client(rally_server, username, password, oauth_key):
        print "Executing create_client() in RallyClient class in RallyClient.py\n"
        return RallyClient(rally_server, username, password, oauth_key)

    def lookup_workspace_id_by_workspace_name(self, workspace_name):
        workspace_query_response = self.rest_api.get("Workspace", fetch="ObjectID", query="Name = %s" % workspace_name)

        if not workspace_query_response.errors:
            workspace = workspace_query_response.next()
            return workspace.ObjectID


    def lookup_user_story_by_formatted_id(self, type, formatted_id, workspace):
        response = self.rest_api.get(type, fetch="ObjectID", query = "FormattedID = %s" % formatted_id, workspace = workspace, projectScopeUp = False, projectScopeDown = True)

        if not response.errors:
            print("Total results: %d\n" % response.resultCount)
            result = response.next()
            return result.ObjectID
        else:
            print("The following errors occurred: ")
            for err in response.errors:
                print("\t" + err)
            return None

    def create_item(self, workspace, properties, user_story_formatted_id, user_story_type, property_type, item_type):
        workspace_ref = self.lookup_workspace_id_by_workspace_name(workspace)
        story_ref = self.lookup_user_story_by_formatted_id(user_story_type, user_story_formatted_id, workspace_ref)

        property_dict = dict(ast.literal_eval(properties))
        property_dict[property_type] = story_ref
        property_dict["Workspace"] = workspace_ref

        item_create_response = self.rest_api.put(item_type, property_dict)

        for error in item_create_response.errors:
            print "Received error: %s\n" % error

        for warning in item_create_response.warnings:
            print "Received warning: %s\n" % warning

        if not item_create_response.errors:
            print "Executed successful on Rally"
            return item_create_response.FormattedID
        else:
            raise Exception("Failed to create record in Rally")


    def update_item(self, workspace, properties, user_story_formatted_id, user_story_type):
        workspace_ref = self.lookup_workspace_id_by_workspace_name(workspace)
        story_ref = self.lookup_user_story_by_formatted_id(user_story_type, user_story_formatted_id, workspace_ref)
        property_dict = dict(ast.literal_eval(properties))
        property_dict["Workspace"] = workspace_ref

        update_response = self.rest_api.post(user_story_type, property_dict)

        for error in update_response.errors:
            print "Received error: %s\n" % error

        for warning in update_response.warnings:
            print "Received warning: %s\n" % warning

        if not update_response.errors:
            print "Executed successful on Rally"
            return update_response.FormattedID
        else:
            raise Exception("Failed to update record in Rally")
