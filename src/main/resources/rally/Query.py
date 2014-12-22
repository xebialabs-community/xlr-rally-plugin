#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json

RECORD_CREATED_STATUS = 201

if rallyServer is None:
    print "No server provided."
    sys.exit(1)

rallyUrl = rallyServer['url']

credentials = CredentialsFallback(rallyServer, username, password).getCredentials()

rallyAPIUrl = rallyUrl + '/api/now/v1/table/' + tableName

rallyResponse = XLRequest(rallyAPIUrl, 'GET', content, credentials['username'], credentials['password'], 'application/json').send()

if rallyResponse.status == RECORD_CREATED_STATUS:
    data = json.loads(rallyResponse.read())
    sysId = data["result"]["sys_id"]
    print "Executed %s on Rally." % (sysId)
else:
    print "Failed to create record in Rally"
    rallyResponse.errorDump()
    sys.exit(1)

