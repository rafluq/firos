from include.pubsub.genericPubSub import Subscriber
from include.ros.topicHandler import RosTopicHandler


class SomeExampleSubscriber(Subscriber):
    '''
        This class just needs to inherit Subscriber.

        You can here specify your own Routine which should happen. 
        This class subscribes to data (which FIROS receives).
    '''




    def subscribe(self, robotID, topicList, msgDefinitions):
        # Here goes the Subscription Routine
        # This Routine needs to be called somehow from an extern Signal
        # In cbSubscriber it is directly called from the Web-Server (conveniently!)

        # You need to make in this Routine sure (it is only called ONCE), that you have some
        # mechanism, which calls the described function below!
        #
        # Also you need to make sure to call RosTopicHandler.publish to forward this Message
        # to the ROS-World
        #
        # RosTopicHandler.publish("ROBOT_ID", "TOPIC", "CONVERTED_DATA", "DATA_STRUCT")
        #
        # where CONVERTED_DATA is ROS-conform!
        # where DATA_STRUCT is: {"type": "STRING_OF_MESSAGE_TYPE_WITH_POINT"}
        
        pass
    
    def unsubscribe(self):
        # Here goes the Routine which needs to be done to unsubscribe
        # It is called automatically!
        pass
