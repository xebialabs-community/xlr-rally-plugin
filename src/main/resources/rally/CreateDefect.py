#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import ast
from com.google.gson import JsonObject
from com.rallydev.rest import RallyRestApi
from com.rallydev.rest.request import CreateRequest

from rally.RallyClientUtil import Rally_Client_Util

rallyClient = Rally_Client_Util.create_rally_client()

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
    restApi = RallyRestApi(URI(rallyUrl), oAuthKey);
else:
    restApi = RallyRestApi(URI(rallyUrl), credentials['username'], credentials['password'])

workspaceRef = rallyClient.lookup_workspace_id_by_workspace_name(restApi, workspace)

storyRef = rallyClient.lookup_user_story_by_formatted_id(restApi, "HierarchicalRequirement", userStoryFormattedId, workspaceRef)

newDefect = JsonObject()
propertyDict = dict(ast.literal_eval(properties))
for key, value in propertyDict.iteritems():
    newDefect.addProperty(key, value);
newDefect.addProperty("Requirement", storyRef);

defectCreateRequest = CreateRequest("defect", newDefect);
defectCreateResponse = restApi.create(defectCreateRequest);

rallyResult = defectCreateResponse.wasSuccessful()
print "Create defect result: %s\n" % rallyResult

errors = defectCreateResponse.getErrors()
for error in errors:
    print "Received error: %s\n" % error

warnings = defectCreateResponse.getWarnings()
for warning in warnings:
    print "Received warning: %s\n" % warning

if rallyResult:
    print "Executed successful on Rally"
    formattedId = defectCreateResponse.getObject().get('FormattedID').getAsString()
else:
    print "Failed to create record in Rally"
    sys.exit(1)
