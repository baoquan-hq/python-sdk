class ServerException(Exception):
    def __init__(self, request_id, message, timestamp):
        self.request_id = request_id
        self.message = message
        self.timestamp = timestamp
