#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from rally.RallyClientUtil import RallyClientUtil
import logging

if rallyServer is None:
    print "No server provided."
    sys.exit(1)

rally_client = RallyClientUtil.create_rally_client(
    rallyServer, username, password, oAuthKey
)

rallyResponse = rally_client.query(
    workspace, project, rally_type, query=query, fetch="True", rollupdata=True
)
logging.debug("Query Status - rallyResponse =  %s" % rallyResponse)
logging.debug("Query Status - rallyResponse.content =  %s" % rallyResponse.content)

status = "OK"
print ("|  ID | Name | Status |")
print ("|-----|-----------|-------------|")
rows = {}
for item in rallyResponse:
    if rally_type == "Task":
        theState = item.State
    else:
        theState = item.ScheduleState

    print ("| %s | %s | %s |" % (item.FormattedID, item.Name, theState))

    # optionally filter the output
    includeInOutput = False
    if filterState is not None:
        if theState in filterState:
            includeInOutput = True
    else:
        includeInOutput = True

    if includeInOutput == True:
        rows[item.FormattedID] = (
            "%s - %s" % (item.Name, theState) if item.Name else "None"
        )

    # Changed this to run the test only if requiredState has been set
    #       requiredState is no longer a required field
    if requiredState is not None and len(requiredState) > 0:
        logging.debug(
            'Testing current state "%s" against required state "%s"'
            % (theState, requiredState)
        )
        if theState != requiredState:
            logging.debug("...failed match")
            status = "Fail"

rallyResult = rows
if status == "Fail":
    exit(-1)
