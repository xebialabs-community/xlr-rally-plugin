#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import ast
from com.google.gson import JsonObject
from com.rallydev.rest import RallyRestApi
from com.rallydev.rest.request import UpdateRequest

from rally.RallyClientUtil import RallyClientUtil

rallyClient = RallyClientUtil.create_rally_client()

if rallyServer is None:
    print "No server provided."
    sys.exit(1)

if properties is None:
    print "No properties provided."
    sys.exit(1)

rallyUrl = rallyServer['url']

credentials = CredentialsFallback(rallyServer, username, password).getCredentials()

restApi = None
if oAuthKey:
    restApi = RallyRestApi(URI(rallyUrl), oAuthKey)
else:
    restApi = RallyRestApi(URI(rallyUrl), credentials['username'], credentials['password'])

content = JsonObject()
propertyDict = dict(ast.literal_eval(properties))
for key, value in propertyDict.iteritems():
    content.addProperty(key, value)

workspace_ref = rallyClient.lookup_workspace_id_by_workspace_name(restApi, workspace)
objectId = rallyClient.lookup_user_story_by_formatted_id(restApi, rally_type, formattedID, workspace_ref)

updateRequest = UpdateRequest("/%s/%s" % (rally_type,objectId), content)
updateResponse = restApi.update(updateRequest)

rallyResult = updateResponse.wasSuccessful()
print "User Story updated result: %s \n" % rallyResult

errors = updateResponse.getErrors()
for error in errors:
    print "Received error: %s \n" % error
