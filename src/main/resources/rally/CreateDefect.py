#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from rally.RallyClientUtil import RallyClientUtil


if rallyServer is None:
    print "No server provided."
    sys.exit(1)

if properties is None:
    print "No properties provided."
    sys.exit(1)

rally_client = RallyClientUtil.create_rally_client(rallyServer, username, password, oAuthKey)
formattedId = rally_client.create_item(workspace, properties, userStoryFormattedId, "HierarchicalRequirement", "Requirement", "defect")
