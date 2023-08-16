#2**
OK = 200
#4**
BAD_REQUEST = 400
"""use when not valid data"""
UNAUTHORIZED = 401
NOT_FOUND = 404
CONFLICT = 409
"""use it when the uniqueness of the data is violated when requesting an insert or update in the database"""

#5**
INTERNAL_SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503
"""use when the service has been disabled"""