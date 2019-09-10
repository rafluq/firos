from include.pubsub.genericPubSub import Publisher


class SomeExamplePublisher(Publisher):
    '''
        This class just needs to inherit Publisher.

        You can here specify your own Routine which should happen. 
        This class publishes the data (which FIROS receives).
    '''


    def publish(self, robotID, topic, rawMsg, msgDefinitions):
        # Here goes the Routine to publish something
        # It is called automatically!
        pass
    
    def unpublish(self):
        # Here goes the Routine which is needed to unpublish
        # It is called automatically!
        pass