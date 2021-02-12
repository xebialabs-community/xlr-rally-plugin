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

def get_row_data(item):
    row_map = {}
    row_map['id'] = item.FormattedID
    row_map['oid'] = item.oid
    row_map['name'] = item.Name if item.Name else "None"
    row_map['readyblocked'] = "Ready" if item.Ready else "Blocked" if hasattr(item, 'Blocked') and item.Blocked else "None"
    row_map['schedulestate'] = item.ScheduleState if hasattr(item, 'ScheduleState') and item.ScheduleState else "Undefined"
    row_map['owner'] = item.Owner.DisplayName if item.Owner else "None"
    row_map['project'] = item.Project.Name if item.Project else "None"
    row_map['link'] = item._ref.replace("slm/webservice/v2.0","#/detail")
    return row_map

if rallyServer is None:
    print "No server provided."
    sys.exit(1)
rallyUrl = rallyServer['url'].rstrip("/")



rally_client = RallyClientUtil.create_rally_client(rallyServer, username, password, oAuthKey)
rallyResult = rally_client.query(workspace, project, itemType, query=query, fetch="FormattedID,oid,Name,Ready,Blocked,Owner,ScheduleState,Project", rollupdata=rollupdata)

rows = {}
for item in rallyResult:
    rows[item.oid] = get_row_data(item)
data = rows    