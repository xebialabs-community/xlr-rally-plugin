#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from rally.RallyClient import RallyClient

class RallyClientUtil(object):

    @staticmethod
    def create_rally_client():
        print "Executing create_rally_client() in RallyClientUtil class in RallyClientUtil.py\n"
        return RallyClient.create_client()
