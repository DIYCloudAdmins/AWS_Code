from datetime import datetime, timezone


def getTagValue(listOfTagDicts: list, keyToInspect: str)->bool:
        '''inspects a list of tag dictionaries for Key == keyToInspect
           If Key exists returns value of that key.
           Otherwise returns None'''
        
        tagList = listOfTagDicts
        keyToInspect = keyToInspect

        retValue = None

        for tags in tagList:
            if tags['Key'] == keyToInspect:
                retValue = tags['Value']
        
        return retValue


def hoursSinceCreation(creationTime: datetime)->bool:
    '''Accepts a time stamp
    Such as stamp returned from EC2 instance['launchTime']
     and returns number of hours passed'''

    timeDiff = datetime.now(timezone.utc) - creationTime
    hoursSinceCreation = (int(timeDiff.seconds)/60)/60
    
    return hoursSinceCreation