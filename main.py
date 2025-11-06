from flask import Flask, request, jsonify
from telethon import TelegramClient, events
import asyncio

API_ID = 33886333
API_HASH = "979753e6fdb91479f7153d533788e87f"
SESSION = "askplex_session"
TARGET = "askplexbot"  # @ हटाकर

app = Flask(__name__)
loop = asyncio.get_event_loop()
client = TelegramClient(SESSION, API_ID, API_HASH, loop=loop)

@app.route("/send", methods=["POST"])
def send_and_get():
    data = request.get_json(force=True)
    q = (data or {}).get("question", "").strip()
    if not q:
        return jsonify({"ok": False, "error": "Question missing"}), 400

    async def run():
        await client.send_message(TARGET, q)
        msg = await client.wait_for(events.NewMessage(from_users=TARGET), timeout=30)
        return msg.message.message

    try:
        reply = loop.run_until_complete(run())
        return jsonify({"ok": True, "reply": reply})
    except asyncio.TimeoutError:
        return jsonify({"ok": False, "error": "Timeout (no reply)"}), 408

if __name__ == "__main__":
    client.start()  # first time: phone + OTP
    app.run(host="0.0.0.0", port=8080)
