# MIT License
#
# Copyright (c) <2015> <Ikergune, Etxetar>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import copy
import json
import urllib2

from include.logger import Log
from include.constants import CONTEXTBROKER, SUBSCRIPTION_LENGTH

# PubSub Handlers
from include.pubsub.contextbroker.cbPublisher import CbPublisher

contexts = {}
Publisher = CbPublisher()


def registerContext(entity_id, data_type, robot,  isPattern=False):
    url = "http://{}:{}/NGSI9/registerContext".format(CONTEXTBROKER["ADDRESS"], CONTEXTBROKER["PORT"])
    attributes = topics2NGSI9(robot)
    current_path = os.path.dirname(os.path.abspath(__file__))
    json_path = current_path.replace("scripts/include/pubsub/contextbroker", "config/robotdescriptions.json")
    description_data = json.load(open(json_path))
    if entity_id in description_data:
        attributes.append({
            "name": "descriptions",
            "type":"publisher:DescriptionData",
            "isDomain": "false"
        })
    data = {
        "contextRegistrations": [
            {
                "entities": [
                    {
                        "type": data_type,
                        "isPattern": "false",
                        "id": entity_id
                    }
                ],
                "attributes": attributes,
                "providingApplication": "http://{}:{}/{}".format(CONTEXTBROKER["ADDRESS"], CONTEXTBROKER["PORT"], CONTEXTBROKER["PROTOCOL"])
            }
        ],
        "duration": SUBSCRIPTION_LENGTH
    }
    response_body = _sendRequest(url, json.dumps(data))
    if response_body != None:
        if "registrationId" in response_body:
            contexts[entity_id] = {
                "data": data,
                "registrationId": response_body["registrationId"]
            }

            if entity_id in description_data:
                _descs = ""
                for link in description_data[entity_id]["descriptions"]:
                    _descs =  _descs + "||" + link
                Publisher.publish(entity_id, data_type, [{
                    "name" : "descriptions",
                    "type" : "DescriptionData",
                    "value" : _descs[2:]
                }])

def deleteAllContexts():
    for key in contexts:
        deleteContext(key)

def deleteContext(entity_id, delete=False):
    if entity_id in contexts:
        url = "http://{}:{}/NGSI9/registerContext".format(CONTEXTBROKER["ADDRESS"], CONTEXTBROKER["PORT"])
        data = {
            "contextRegistrations": [
                {
                    "providingApplication": "http://{}:{}/{}".format(CONTEXTBROKER["ADDRESS"], CONTEXTBROKER["PORT"], CONTEXTBROKER["PROTOCOL"])
                }
            ],
            "duration": "P0D",
            "registrationId": contexts[entity_id]["registrationId"]
        }
        response = _sendRequest(url, json.dumps(data))
        if delete:
            del contexts[entity_id]

def refreshAllContexts():
    for key in contexts:
        refreshContext(key)

def refreshContext(entity_id):
    url = "http://{}:{}/NGSI9/registerContext".format(CONTEXTBROKER["ADDRESS"], CONTEXTBROKER["PORT"])
    data = copy.deepcopy(contexts[entity_id]["data"])
    data["registrationId"] = contexts[entity_id]["registrationId"]
    response = _sendRequest(url, json.dumps(data))

def topics2NGSI9(robot):
    return iterateTopics(robot["publisher"], "publisher") + iterateTopics(robot["subscriber"], "subscriber")

def iterateTopics(topics, topic_type):
    elems = []
    for key in topics:
        elems.append( {
            "name": key,
            "type": topic_type + ":" + topics[key]["class"]._type.replace("/", ".msg."),
            "isDomain": "false"
        })
    return elems


def _sendRequest(url, data, method=None):
    try:
        request = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Accept': 'application/json'})
        if method is not None:
            request.get_method = lambda: method
        response = urllib2.urlopen(request)
        data = response.read()
        response_body = json.loads(data)
        response.close()
        return response_body
    except Exception as ex:
            Log("ERROR", ex.reason)
            return None