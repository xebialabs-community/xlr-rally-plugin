#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from com.rallydev.rest.request import QueryRequest
from com.rallydev.rest.util import Fetch, QueryFilter
from com.google.gson import JsonObject, JsonParser

class Rally_Client(object):

    def __init__(self):
        print "Initializing Rally_Client\n"

    @staticmethod
    def create_client():
        print "Executing create_client() in Rally_Client class in RallyClient.py\n"
        return Rally_Client()

    def lookup_workspace_id_by_workspace_name(self, restApi, workspaceName):
        request = QueryRequest("Workspace")
        request.setQueryFilter(QueryFilter("Name", "=", workspaceName))
        request.setFetch(Fetch(["ObjectId"]))

        workspaceQueryResponse = restApi.query(request)

        if workspaceQueryResponse.wasSuccessful():
            result = workspaceQueryResponse.getResults()
            parser = JsonParser()
            object = (parser.parse(result.toString())).get(0).getAsJsonObject()
            return object.get("ObjectID").getAsString()

    def lookup_user_story_by_formatted_id(self, restApi, type, formattedId, workspace):
        request = QueryRequest(type)
        request.setWorkspace(workspace)
        request.setScopedDown(True)
        request.setScopedUp(False)
        request.setFetch(Fetch(["ObjectID"]))
        request.setQueryFilter(QueryFilter("FormattedID", "=", formattedId))
        queryResponse = restApi.query(request);

        if queryResponse.wasSuccessful():
            print("Total results: %d\n" % queryResponse.getTotalResultCount())
            for result in queryResponse.getResults():
                story = result.getAsJsonObject()
                return story.get("_ref").getAsString()
        else:
            print("The following errors occurred: ");
            for err in queryResponse.getErrors():
                print("\t" + err);
            return None

