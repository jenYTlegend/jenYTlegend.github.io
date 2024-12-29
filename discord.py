import discord
from flask import Flask, request, jsonify
import os
import asyncio
from threading import Thread

# 初始化 Flask 應用
app = Flask(__name__)

# 初始化 Discord 客戶端
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Discord Bot Token（請替換為你的 Bot Token）
DISCORD_TOKEN = 'MTMyMjgzNDQwMzM0NDUxOTE4OA.Gw5pJO.Ygbzic_4xO-LmBPoNztbIaNdk8QNS_QD8fbXp0'

# Flask 路由：接收來自網站的資料並發送到 Discord
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_id = data.get('userId')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({"success": False, "message": "Missing userId or message"}), 400

    try:
        # 使用 asyncio.run() 來運行異步的 Discord.py 操作
        asyncio.run(send_discord_message(user_id, message))
        return jsonify({"success": True, "message": "Message sent!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

async def send_discord_message(user_id, message):
    """使用異步函數發送 Discord 訊息"""
    user = await client.fetch_user(int(user_id))
    if user:
        await user.send(message)
    else:
        raise Exception(f"User with ID {user_id} not found.")

# 事件：當 Discord Bot 登錄成功後，會顯示 Bot 的狀態
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# 啟動 Discord Bot
def start_bot():
    client.run(DISCORD_TOKEN)

# 啟動 Flask 伺服器
def start_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    # 啟動 Flask 伺服器在一個新線程中
    flask_thread = Thread(target=start_flask)
    flask_thread.start()

    # 啟動 Discord Bot
    start_bot()
