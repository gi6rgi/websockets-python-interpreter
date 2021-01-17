import websockets
import asyncio
import logging
from datetime import datetime
from websockets import WebSocketClientProtocol
from asyncio.subprocess import Process


logging.basicConfig(filename='log', level=logging.INFO)


class CodeExecutor:

    @staticmethod
    async def _stream_transfer(proc: Process, ws: WebSocketClientProtocol) -> None:
        """Processes stout/err from the process pipe;
        Sends realtime output through the websocket.
        """
        while True:
            output = await proc.stdout.readline()
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
        proc = await asyncio.create_subprocess_exec(
            'python3', '-u', '-c', sanitized_input,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        await self._stream_transfer(proc, ws)


class Server(CodeExecutor):

    @staticmethod
    async def code_logger(code_text: str, ws: WebSocketClientProtocol) -> None:
        """User input logger."""
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        logging.info(f'{dt_string}\n'
                     f'{ws.remote_address}\n'
                     f'{code_text}\n')

    async def connectin_handler(self, ws: WebSocketClientProtocol, uri: str) -> None:
        async for code_text in ws:
            await self.execute_code(code_text, ws)
            await self.code_logger(code_text, ws)


if __name__ == '__main__':
    server = Server()
    start_server = websockets.serve(server.connectin_handler, 'localhost', 3000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
