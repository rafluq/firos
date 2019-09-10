# MIT License
# 
# Copyright (c) 2019 Fraunhofer IML
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import abc
import inspect
import importlib

# ABC compatibility with Python 2 and 3
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()}) 

class Publisher(ABC):
    '''
        Abstract Publisher. Import this and set it as base 
        to write your own Publisher 
    '''

    @abc.abstractmethod
    def publish(self, robotID, topic, rawMsg, msgDefinitions):
        pass
    
    @abc.abstractmethod
    def unpublish(self):
        pass


class Subscriber(ABC):
    '''
        Abstract Subscriber. Import this and set it as base 
        to write your own Subscriber 
    '''

    @abc.abstractmethod
    def subscribe(self, robotID, topicList, msgDefinitions):
        pass
    
    @abc.abstractmethod
    def unsubscribe(self):
        pass


class PubSub(object):
    '''
        TODO add description
    '''

    publishers = []
    subscribers = []

    def __init__(self):
        '''
            imports all publisher and subscriber and saves them into the list.

            We retreive here all classes which
        '''
        folder = os.path.dirname(os.path.realpath(__file__))
        folderInfo = os.listdir(folder)


        # Get subfolders
        subfolders = {}
        for fi in folderInfo:
            if not fi.startswith("_") and os.path.isdir(folder + os.path.sep + fi):
                subfolders[fi] = {}

        # Get Files inside subfolders
        for i in subfolders.keys():
            for r, d, files in os.walk(folder + os.path.sep + i):
                for f in files:
                    if not f.startswith("_"):
                        subfolders[i][f.split(".")[0]] = None
                    
        for fold in subfolders.keys():
            for fil in subfolders[fold].keys():
                module_def = "include.pubsub." + fold + "." + fil
                __import__(module_def) # module needs to be imported manually!
                clsmembers = inspect.getmembers(sys.modules[module_def], \
                    lambda member: inspect.isclass(member) and member.__module__ == module_def)
                for clazz in clsmembers:
                    subfolders[fold][fil] = clazz[1]

        # Distinguish between Subscribers and Publishers
        for fold in subfolders.keys():
            for fil in subfolders[fold].keys():
                if subfolders[fold][fil].__base__ is Subscriber:
                    # We found a Subscriber
                    self.subscribers.append(subfolders[fold][fil]())
                elif subfolders[fold][fil].__base__ is Publisher:
                    # We found a Publisher
                    self.publishers.append(subfolders[fold][fil]())
                else:
                    # We do nothing to other classes
                    pass

        pass




    def publish(self, robotID, topic, rawMsg, msgDefinitions):
        for pub in self.publishers:
            pub.publish(robotID, topic, rawMsg, msgDefinitions)

    
    def unpublish(self):
        for pub in self.publishers:
            pub.unpublish()

    def subscribe(self, robotID, topicList, msgDefinitions):
        for sub in self.subscribers:
            sub.subscribe(robotID, topicList, msgDefinitions)
    
    def unsubscribe(self):
        for sub in self.subscribers:
            sub.unsubscribe()

