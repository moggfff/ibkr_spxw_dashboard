# -*- coding: utf-8 -*-
import os, requests, json

class Notifier:
    def __init__(self, cfg: dict):
        self.enabled = cfg.get("telegram",{}).get("enabled", True)
        self.token = cfg.get("telegram",{}).get("bot_token", "")
        self.chat_id = cfg.get("telegram",{}).get("chat_id", "")

    def send(self, text: str):
        if not self.enabled or not self.token or not self.chat_id:
            return False
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            r = requests.post(url, data={"chat_id": self.chat_id, "text": text}, timeout=10)
            return r.ok
        except Exception as e:
            print("Notifier error:", e)
            return False
