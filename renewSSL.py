# Copyright (C) 2022  un-lock-able
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os.path
import sys

from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkcore.client import AcsClient

accessKeyId = ""
accessSecret = ""
client = None


def add_record(domain_name, RR, value):
    request = AddDomainRecordRequest()
    request.set_accept_format("json")
    request.set_DomainName(domain_name)
    request.set_RR(RR) # RR is the host name like live, www or @
    request.set_Type("TXT")
    request.set_TTL(60)
    request.set_Value(value)
    response = client.do_action_with_exception(request)
    # print(json.loads(response))


def remove_record(record_id):
    request = DeleteDomainRecordRequest()
    request.set_accept_format("json")
    request.set_RecordId(record_id)
    response = client.do_action_with_exception(request)


def check_record(domain_name, domain_name_with_subdomain):
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format("json")
    request.set_DomainName(domain_name)
    request.set_SubDomain(domain_name_with_subdomain)
    request.set_Type("TXT")
    response = client.do_action_with_exception(request)
    response = json.loads(response)
    return response["DomainRecords"]["Record"][0]["RecordId"]


def main():
    global accessKeyId, accessSecret, client
    arg_list = sys.argv
    action = arg_list[1]
    if action not in ["delete", "create"]:
        print("Unknown action, script ended")
        return
    domain = arg_list[2]
    domain_with_subdomain = arg_list[3]
    token = arg_list[4]
    with open(os.path.join(os.path.dirname(arg_list[0]), "./settings.json")) as setting_file:
        settings = json.loads(setting_file.read())
    accessKeyId = settings["accessKeyId"]
    accessSecret = settings["accessSecret"]
    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
    if action == "create":
        add_record(domain, domain_with_subdomain[:(len(domain_with_subdomain)-len(domain)-1)], token)
    elif action == "delete":
        remove_record(check_record(domain, domain_with_subdomain))


if __name__ == "__main__":
    main()