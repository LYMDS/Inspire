import uuid
def Guid():
    return uuid.uuid4().__str__()

def IsGuid(id):
    return id != None and id != '' and len(id) == 36