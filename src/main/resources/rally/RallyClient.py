#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from com.rallydev.rest.request import QueryRequest
from com.rallydev.rest.util import Fetch, QueryFilter
from com.google.gson import JsonParser

class RallyClient(object):

    def __init__(self):
        print "Initializing RallyClient\n"

    @staticmethod
    def create_client():
        print "Executing create_client() in RallyClient class in RallyClient.py\n"
        return RallyClient()

    def lookup_workspace_id_by_workspace_name(self, rest_api, workspace_name):
        request = QueryRequest("Workspace")
        request.setQueryFilter(QueryFilter("Name", "=", workspace_name))
        request.setFetch(Fetch(["ObjectId"]))

        workspace_query_response = rest_api.query(request)

        if workspace_query_response.wasSuccessful():
            result = workspace_query_response.getResults()
            parser = JsonParser()
            object = (parser.parse(result.toString())).get(0).getAsJsonObject()
            return object.get("ObjectID").getAsString()

    def lookup_user_story_by_formatted_id(self, rest_api, type, formatted_id, workspace):
        request = QueryRequest(type)
        request.setWorkspace(workspace)
        request.setScopedDown(True)
        request.setScopedUp(False)
        request.setFetch(Fetch(["ObjectID"]))
        request.setQueryFilter(QueryFilter("FormattedID", "=", formatted_id))
        query_response = rest_api.query(request)

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

