
if not window.bdchecker?
  window.bdchecker = {}

onload = () =>

  textarea = document.getElementById("id_user_input")

  window.bdchecker.codemirror = CodeMirror.fromTextArea textarea,
    mode: 'text/x-plsql',
    theme: 'base16-dark'

window.onload = onload