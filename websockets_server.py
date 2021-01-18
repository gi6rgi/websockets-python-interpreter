import websockets
import asyncio
import logging
import sys
from config import TIMEOUT
from datetime import datetime
from websockets import WebSocketClientProtocol
from asyncio.subprocess import Process


logging.basicConfig(filename='log', level=logging.INFO)


class CodeExecutor:

    def __init__(self, timeout: int):
        self.timeout = timeout

    @staticmethod
    async def _stream_transfer(process: Process, ws: WebSocketClientProtocol) -> None:
        """Captures stdout/err from the process pipe;
        Sends output data through the websocket.
        """
        while True:
            output = await process.stdout.readline()
            output = output.decode()
            if output:
                await ws.send(output[:-1])
            else:
                break

    async def execute_code(self, code_text: str, ws: WebSocketClientProtocol) -> None:
        """Executes user code.
        
        '-u' flag - totally unbuffered stdout/err;
        Imports module to sanitize user input;
        Provides realtime stdout stream.
        """
        sanitized_input = f'import sanitizer.sanitizer\n{code_text}'
        process = await asyncio.create_subprocess_exec(
            'python3', '-u', '-c', sanitized_input,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        try:
            await asyncio.wait_for(self._stream_transfer(process, ws), self.timeout)
        except asyncio.TimeoutError:
            await ws.send('TimeoutError')


class Server(CodeExecutor):

    def __init__(self, timeout: int):
        super().__init__(timeout)

    @staticmethod
    def _get_server_time():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    async def _code_logger(self, code_text: str, ws: WebSocketClientProtocol) -> None:
        """User input logger."""
        dt_string = self._get_server_time()
        logging.info(f'{dt_string}\n'
                     f'{ws.remote_address}\n'
                     f'{code_text}\n')

    async def connectin_handler(self, ws: WebSocketClientProtocol, uri: str) -> None:
        await ws.send(sys.version)
        async for code_text in ws:
            await self.execute_code(code_text, ws)
            await self._code_logger(code_text, ws)


if __name__ == '__main__':
    server = Server(TIMEOUT)
    start_server = websockets.serve(server.connectin_handler, '0.0.0.0', 3000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
