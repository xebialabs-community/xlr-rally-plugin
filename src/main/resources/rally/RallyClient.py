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
from com.rallydev.rest import RallyRestApi
from com.rallydev.rest.request import CreateRequest, QueryRequest, UpdateRequest
from com.rallydev.rest.util import Fetch, QueryFilter
from com.google.gson import JsonObject, JsonParser
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
            self.rest_api = RallyRestApi(URI(rally_url), oauth_key)
        else:
            self.rest_api = RallyRestApi(URI(rally_url), credentials['username'], credentials['password'])
        if self.rally_server['proxyHost']:
            self.rest_api.setProxy(URI("http://%s:%s" % (self.rally_server['proxyHost'], self.rally_server['proxyPort'])))


    @staticmethod
    def create_client(rally_server, username, password, oauth_key):
        print "Executing create_client() in RallyClient class in RallyClient.py\n"
        return RallyClient(rally_server, username, password, oauth_key)

    def lookup_workspace_id_by_workspace_name(self, workspace_name):
        request = QueryRequest("Workspace")
        request.setQueryFilter(QueryFilter("Name", "=", workspace_name))
        request.setFetch(Fetch(["ObjectId"]))

        workspace_query_response = self.rest_api.query(request)

        if workspace_query_response.wasSuccessful():
            result = workspace_query_response.getResults()
            parser = JsonParser()
            object = (parser.parse(result.toString())).get(0).getAsJsonObject()
            return object.get("ObjectID").getAsString()


    def lookup_user_story_by_formatted_id(self, type, formatted_id, workspace):
        request = QueryRequest(type)
        request.setWorkspace(workspace)
        request.setScopedDown(True)
        request.setScopedUp(False)
        request.setFetch(Fetch(["ObjectID"]))
        request.setQueryFilter(QueryFilter("FormattedID", "=", formatted_id))
        query_response = self.rest_api.query(request)

        if query_response.wasSuccessful():
            print("Total results: %d\n" % query_response.getTotalResultCount())
            for result in query_response.getResults():
                story = result.getAsJsonObject()
                return story.get("_ref").getAsString()
        else:
            print("The following errors occurred: ")
            for err in query_response.getErrors():
                print("\t" + err)
            return None

    def create_item(self, workspace, properties, user_story_formatted_id, user_story_type, property_type, item_type):
        workspace_ref = self.lookup_workspace_id_by_workspace_name(workspace)
        story_ref = self.lookup_user_story_by_formatted_id(user_story_type, user_story_formatted_id, workspace_ref)

        new_item = JsonObject()
        property_dict = dict(ast.literal_eval(properties))
        for key, value in property_dict.iteritems():
            new_item.addProperty(key, value)
        new_item.addProperty(property_type, story_ref)

        item_create_request = CreateRequest(item_type, new_item)
        item_create_response = self.rest_api.create(item_create_request)

        rally_result = item_create_response.wasSuccessful()
        print "Create item result: %s\n" % rally_result

        errors = item_create_response.getErrors()
        for error in errors:
            print "Received error: %s\n" % error

        warnings = item_create_response.getWarnings()
        for warning in warnings:
            print "Received warning: %s\n" % warning

        if rally_result:
            print "Executed successful on Rally"
            return item_create_response.getObject().get('FormattedID').getAsString()
        else:
            raise Exception("Failed to create record in Rally")


    def update_item(self, workspace, properties, user_story_formatted_id, user_story_type):
        workspace_ref = self.lookup_workspace_id_by_workspace_name(workspace)
        story_ref = self.lookup_user_story_by_formatted_id(user_story_type, user_story_formatted_id, workspace_ref)
        content = JsonObject()
        property_dict = dict(ast.literal_eval(properties))
        for key, value in property_dict.iteritems():
            content.addProperty(key, value)

        update_request = UpdateRequest("/%s/%s" % (user_story_type, story_ref), content)
        update_response = self.rest_api.update(update_request)

        rally_result = update_response.wasSuccessful()
        print "User Story updated result: %s \n" % rally_result

        errors = update_response.getErrors()
        for error in errors:
            print "Received error: %s \n" % error

        return rally_result
