import threading

# Create a thread-local variable to store the request object
request_local = threading.local()