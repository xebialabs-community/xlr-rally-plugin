#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from rally.RallyClientUtil import RallyClientUtil

if rallyServer is None:
    print "No server provided."
    sys.exit(1)

rally_client = RallyClientUtil.create_rally_client(rallyServer, username, password, oAuthKey)

rallyResult = rally_client.query(workspace, project, rally_type, query="FormattedID = %s" % userStoryFormattedId, fetch="True", rollupdata=True)
if rallyResult.resultCount != 1:
    raise Exception("Did not find 1 unique item")
status = "Undefined"
item = rallyResult.next()
if item.Ready:
    status = "Ready"
if hasattr(item, 'Blocked') and item.Blocked:
    status = "Blocked"