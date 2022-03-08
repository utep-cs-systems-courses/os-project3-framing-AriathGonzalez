def frameWriter(socket, data):
    while len(data):
        bytesSent = socket.send(data)
        data = data[bytesSent:]
    # Send via socket, frame by frame until empty
