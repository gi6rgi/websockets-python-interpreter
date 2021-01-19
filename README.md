## http://176.118.165.85/ 
### Features
- stdout/stderr отображается в правом окне
- Таймаут задаётся в файле config.py. На примере ниже его значение равно 5

*на сервере таймаут равен 30 секундам


<img src="https://github.com/ge6rgii/websockets-python-interpreter/blob/main/examples/timeouterr.gif" width=600px>


- Запрещены импорты некоторых библиотек и использование методов open, exec и eval
<img src="https://github.com/ge6rgii/websockets-python-interpreter/blob/main/examples/cheetoslock.jpg" width=600px>

### На всякий случай для удобства:
- git clone https://github.com/ge6rgii/websockets-python-interpreter && cd websockets-python-interpreter
- docker-compose up

сервис будет доступен на localhost:3030
