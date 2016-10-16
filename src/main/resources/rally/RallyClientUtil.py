#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from rally.RallyClient import Rally_Client

class Rally_Client_Util(object):

    @staticmethod
    def create_rally_client():
        print "Executing create_rally_client() in Rally_Client_Util class in RallyClientUtil.py\n"
        return Rally_Client.create_client()
