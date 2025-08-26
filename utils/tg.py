# -*- coding: utf-8 -*-
# utils/tg.py
import json, requests, sys

def load_cfg():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def send_tg(text: str):
    cfg = load_cfg().get("telegram", {})
    if not (cfg.get("enabled") and cfg.get("bot_token") and cfg.get("chat_id")):
        return
    url = f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage"
    try:
        requests.post(url, data={"chat_id": cfg["chat_id"], "text": text}, timeout=10)
    except Exception:
        pass

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Notification"
    send_tg(msg)
