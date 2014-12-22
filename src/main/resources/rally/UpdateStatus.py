#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import ast
from java.net import URI
from com.rallydev.rest import RallyRestApi
from com.rallydev.rest.request import UpdateRequest, QueryRequest
from com.rallydev.rest.util import Fetch, QueryFilter
from com.google.gson import JsonObject, JsonParser, JsonArray

def lookup_workspace_id_by_workspace_name(rest_api, workspace_name):
    request = QueryRequest("Workspace")
    request.setQueryFilter(QueryFilter("Name", "=", workspace_name))
    request.setFetch(Fetch(["ObjectId"]))

    workspace_query_response = rest_api.query(request)
    if workspace_query_response.wasSuccessful():
        result = workspace_query_response.getResults()
        parser = JsonParser()
        object = (parser.parse(result.toString())).get(0).getAsJsonObject()
        return object.get("ObjectID").getAsString()


def lookup_user_story_by_formatted_id(rest_api, type, formatted_id, workspace):
  request = QueryRequest(type)
  request.setWorkspace(workspace)
  request.setScopedDown(True)
  request.setScopedUp(False)
  request.setFetch(Fetch(["ObjectID"]))
  request.setQueryFilter(QueryFilter("FormattedID", "=", formatted_id))
  query_response = rest_api.query(request);

  if query_response.wasSuccessful():
    print("Total results: %d" % query_response.getTotalResultCount())
    for result in query_response.getResults():
      story = result.getAsJsonObject()
      return story.get("_ref").getAsString()
  else:
    print("The following errors occurred: ");
    for err in query_response.getErrors():
        print("\t" + err);
    return None

if rallyServer is None:
    print "No server provided."
    sys.exit(1)

if properties is None:
    print "No properties provided."
    sys.exit(1)

rallyUrl = rallyServer['url']

credentials = CredentialsFallback(rallyServer, username, password).getCredentials()

# Setup connection
restApi = None
if oAuthKey:
    restApi = RallyRestApi(URI(rallyUrl), oAuthKey);
else:
    restApi = RallyRestApi(URI(rallyUrl), credentials['username'], credentials['password'])

content = JsonObject();
propertyDict = dict(ast.literal_eval(properties))
for key, value in propertyDict.iteritems():
    content.addProperty(key, value);
workspace_ref = lookup_workspace_id_by_workspace_name(restApi, workspace)
objectId = lookup_user_story_by_formatted_id(restApi, rally_type, formattedID, workspace_ref)
updateRequest = UpdateRequest("/%s/%s" % (rally_type,objectId), content);
updateResponse = restApi.update(updateRequest)

rallyResult = updateResponse.wasSuccessful()
print "User Story updated result: %s \n" % rallyResult

errors = updateResponse.getErrors()
for error in errors:
    print "Received error: %s \n" % error

warnings = updateResponse.getWarnings()
for warning in warnings:
    print "Received warning: %s \n" % warning

if rallyResult:
    print "Executed successful on Rally."
else:
    print "Failed to update record in Rally"
    sys.exit(1)

