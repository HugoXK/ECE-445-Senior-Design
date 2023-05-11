# import socket
# import json
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # host = socket.gethostname()
# port = 9999
# s.connect(("127.0.0.1", port))
# msg = s.recv(1024)
# msg = msg.decode('utf-8')
# print(msg)
# s.close()






import socket
import json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostname()
port = 8888
s.connect(("127.0.0.1", port))
# msg = "hi"
msg = {"a":0.01}
msg = json.dumps(msg)
s.sendall(msg.encode('utf-8'))
s.close()
