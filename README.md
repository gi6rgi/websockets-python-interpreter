### Online Python interpreter
 - A WebSocket connection is established between the client and the server, which makes it possible to receive stdout / stderr of the running process in real time (displayed in the right window)
 - The timeout is set in the configuration file. In the example below, its value is 5



<img src="https://github.com/ge6rgii/websockets-python-interpreter/blob/main/examples/timeouterr.gif" width=600px>


- Imports of some libraries and the use of the open, exec and eval functions are prohibited 
<img src="https://github.com/ge6rgii/websockets-python-interpreter/blob/main/examples/cheetoslock.jpg" width=600px>


### How to run locally:
- git clone https://github.com/ge6rgii/websockets-python-interpreter && cd websockets-python-interpreter
- docker-compose up

The service will be available at localhost:3030
