var left_editor = CodeMirror.fromTextArea(document.getElementById("left_terminal"), {
  lineNumbers: true,
  indentUnit: 4
});

var right_editor = CodeMirror.fromTextArea(document.getElementById("right_terminal"), {
  lineNumbers: true,
  readOnly: true,
  cursorBlinkRate: 0,
});

const ws = new WebSocket("ws://localhost:3000");
// Some inkostilation happens here.
curr_line = '';

function sendCode() {
  curr_line = '';
  code = left_editor.getValue();
  ws.send(code);
};

ws.onmessage = msg => {
  curr_line += msg.data + '\n';
  right_editor.setValue(curr_line);
};

ws.onclose = function(event) {
  if (event.wasClean) {
    right_editor.setValue('The connection was closed.');
  } else {
    right_editor.setValue('Сonnection drop-out was detected.'); // например, "убит" процесс сервера
  }
  right_editor.setValue('Code: ' + event.code + ' reason: ' + event.reason);
};