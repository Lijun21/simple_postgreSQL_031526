"""
There is a server where you can store data. 
It has a put method that allows you to save up to 1MB of data per request and return an ID, 
and a get method that given an ID will return the data stored. 
Write a client library that will interact with the server and allow the user to 
store and retrieve arbitrary amounts of data.
"""
############ This is a black box  ###############
"""
This is actually used in real systems:

Write-once storage (logs, backups) — just keep bumping the pointer
PostgreSQL WAL (Write-Ahead Log) — append only, never deletes mid-log
Memory arenas in game engines — allocate fast, free everything at once at the end

"""
class Server:
    # Assume this is a blackbox server that can store up to 1MB of data. You can't modify this class.
    def __init__(self):
        self._data_store = {}
        self._id = 0

    def put(self, data: str):
        ## assume this function stores in persistent storage
        if len(data) > 1<<20:
            raise Exception("exceed 1MB limits")
        self._data_store[self._id] = data
        id = self._id
        self._id += 1
        return id

    def get(self, id: int):
        return self._data_store[id]
############ End of BlackBox ###############

# TODO: implement Client.
class Client:
    def __init__(self):
        pass
    
    def put(self, data: str) -> str:
        pass
    
    def get(self, id: str) -> str:
        pass