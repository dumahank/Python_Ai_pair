from flask import Flask, request, jsonify, render_template_string
import chatbot

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Rule-Based ChatBot</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 40px; }
      #chat { max-width: 600px; margin: 0 auto; }
      .message { padding: 8px; margin: 6px 0; border-radius: 6px; }
      .user { background: #e6f7ff; text-align: right; }
      .bot { background: #f0f0f0; text-align: left; }
    </style>
  </head>
  <body>
    <div id="chat">
      <h1>Rule-Based ChatBot</h1>
      <div id="messages"></div>
      <form id="form">
        <input id="input" autocomplete="off" style="width:80%" placeholder="Say something..." />
        <button>Send</button>
      </form>
    </div>

    <script>
      const form = document.getElementById('form');
      const input = document.getElementById('input');
      const messages = document.getElementById('messages');

      function addMessage(text, cls) {
        const d = document.createElement('div');
        d.className = 'message ' + cls;
        d.textContent = text;
        messages.appendChild(d);
        messages.scrollTop = messages.scrollHeight;
      }

      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        addMessage('You: ' + text, 'user');
        input.value = '';

        const res = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        addMessage('Bot (' + data.category + '): ' + data.response, 'bot');
      });
    </script>
  </body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    return render_template_string(INDEX_HTML)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    message = data.get('message', '')
    response, category = chatbot.respond(message)
    return jsonify({ 'response': response, 'category': category })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
