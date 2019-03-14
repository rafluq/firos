API
===

FIROS has several REST entry points that are used for connecting with the context broker or getting data from FIROS.

You can find FIROS api at http://docs.FIROS.apiary.io/# (OLD)

GET /robots
-----------

Get robots handled by FIROS with their corresponding *topics*. Each *topic* contains the `name`, `type`, `role` and `structure`:

``` json
[
    {
        "name": "turtle1",
        "topics": [
            {
                "type": "turtlesim.msg.Pose",
                "name": "pose",
                "structure": {
                    "y": "float32",
                    "x": "float32",
                    "linear_velocity": "float32",
                    "angular_velocity": "float32",
                    "theta": "float32"
                },
                "pubsub": "subscriber"
            },
            {
                "type": "geometry_msgs.msg.Twist",
                "name": "cmd_vel",
                "structure": {
                    "linear": {
                        "y": "float64",
                        "x": "float64",
                        "z": "float64"
                    },
                    "angular": {
                        "y": "float64",
                        "x": "float64",
                        "z": "float64"
                    }
                },
                "pubsub": "publisher"
            }
        ],
    }
]
```

GET /robot/NAME
---------------

Gets the data which is published/subscribed by the robot in the Context-Broker. Here the contents of the Context Broker is shown.

Here as an example: the content of `turtlesim` with its publishing topic `pose`:

```json
{
    "id":"turtle1",
    "type":"ROBOT",
    "descriptions":{
        "type":"array",
        "value":[
        {
            "type":"string",
            "value":"http://wiki.ros.org/ROS/Tutorials/UsingRxconsoleRoslaunch"
        },
        {
            "type":"string",
            "value":"http://wiki.ros.org/ROS/Tutorials/UnderstandingNodes"
        }
        ],
        "metadata":{

        }
    },
    "pose":{
        "type":"turtlesim.Pose",
        "value":{
        "y":{
            "type":"number",
            "value":5.544444561
        },
        "x":{
            "type":"number",
            "value":5.544444561
        },
        "linear_velocity":{
            "type":"number",
            "value":0
        },
        "theta":{
            "type":"number",
            "value":0
        },
        "angular_velocity":{
            "type":"number",
            "value":0
        }
        },
        "metadata":{
            "dataType":{
                "type":"dataType",
                "value":{
                    "y":"float32",
                    "x":"float32",
                    "linear_velocity":"float32",
                    "theta":"float32",
                    "angular_velocity":"float32"
                }
            }
        }
    }
}
```


POST /firos
-----------

This API handles the subscription data of the context broker. 

POST /robot/connect
-------------------

This API makes FIROS connecting to new robots in case their names and topics match the ones allowed on the *whitelist.json*

POST /robot/disconnect/NAME
--------------------------

This API forces FIROS to disconnect from the robot specified by the *NAME* parameter. It will also delete any connection and entity associated to the particular robot on the Context Broker.


Currently untested POST-Operationes:
----
These Operations might work, but are not tested currently.

POST /whitelist/write
---------------------

This API overwrites or creates entries in the robot *whitelist*. This can be done by sending the following data:

``` json
{
    "turtle\\w+": {
        "publisher": ["cmd_vel"],
        "subscriber": ["pose"]
    },
    "robot\\w+": {
        "publisher": ["cmd_vel.*teleop", ".*move_base/goal"],
        "subscriber": [".*move_base/result"]
    }
}
```

NOTE: In case you want to keep any element, it must be sent along with the ones to be replaced.

EXAMPLE:

Take this *whitelist.json* as a starting point:

``` json
{
    "turtle\\w+": {
        "publisher": ["cmd_vel"],
        "subscriber": ["pose"]
    }
}
```

Now, the following command is sent:

``` json
POST /whitelist/write
{
    "turtle\\w+": {
        "publisher": ["cmd_vel2"],
        "subscriber": []
    }
}
```

The resulting *whitelist* will be as follows:

``` json
{
    "turtle\\w+": {
        "publisher": ["cmd_vel2"],
        "subscriber": []
    }
}
```

POST /whitelist/remove
----------------------

This API removes elements from the *whitelist*. The format is as follows:

``` json
{
    "turtle\\w+": {
        "publisher": [],
        "subscriber": ["pose"]
    },
    "robot\\w+": {
        "publisher": ["cmd_vel.*teleop", ".*move_base/goal"],
        "subscriber": []
    }
}
```

EXAMPLE:

Take this *whitelist.json* as a starting point:

``` json
{
    "turtle\\w+": {
        "publisher": ["cmd_vel"],
        "subscriber": ["pose"]
    },
    "robot\\w+": {
        "publisher": ["cmd_vel.*teleop", ".*move_base/goal"],
        "subscriber": [".*move_base/result"]
    }
}
```

Now, the following json is sent:

``` json
POST /whitelist/remove
{
    "turtle\\w+": {
        "publisher": [],
        "subscriber": ["pose"]
    },
    "robot\\w+": {
        "publisher": ["cmd_vel.*teleop", ".*move_base/goal"],
        "subscriber": []
    }
}
```

The resulting *whitelist* will look as follows:

``` json
{
    "turtle\\w+": {
        "publisher": ["cmd_vel"],
        "subscriber": []
    },
    "robot\\w+": {
        "publisher": [],
        "subscriber": [".*move_base/result"]
    }
}
```

POST /whitelist/restore
-----------------------

This API restores the *whitelist* file to its initial state.

Ent-to-end tests
================

In order to test if FIROS is publishing into ContextBroker you can simply open up any browser and enter the following in the adress-line:
> CONTEXTBROKER_IP:CB_PORT/v2/entities

If the Context-Broker returns a page with content, then everything is working.

For more Context-Broker-Operations visit [this site](https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/index.html)


FIROS Topics
============

FIROS is listening to 2 topics in order to handle robot connections.

/FIROS/connect
--------------

Calling this topic with an empty string will make FIROS connect to new robots in case their names and topics match the ones allowed on the *whitelist.json*


/FIROS/disconnect
-----------------

Disconnecting robots from FIROS is possible by simply calling this topic with the robot name.
`/FIROS/disconnect/turtle1`