#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
from java.net import URI
from com.rallydev.rest import RallyRestApi
from com.rallydev.rest.request import UpdateRequest
from com.google.gson import JsonObject

if rallyServer is None:
    print "No server provided."
    sys.exit(1)

rallyUrl = rallyServer['url']

credentials = CredentialsFallback(rallyServer, username, password).getCredentials()


restApi = RallyRestApi(URI(rallyUrl), oAuthKey);
content = JsonObject();
content.addProperty("FormattedID", formattedID);
content.addProperty("XLEnvironment", environment);
updateRequest = UpdateRequest("/hierarchicalrequirement/11434180156", content);
updateResponse = restApi.update(updateRequest)

rallyResult = updateResponse.wasSuccessful()
print "User Story updated result: %s" % rallyResult

errors = updateResponse.getErrors()
for error in errors:
    print "Received error: %s" % error

warnings = updateResponse.getWarnings()
for warning in warnings:
    print "Received warning: %s" % warning

if rallyResult:
    print "Executed successful on Rally."
else:
    print "Failed to update record in Rally"
    sys.exit(1)

