# -*- coding: utf-8 -*-
import os, json, time, threading
from flask import Flask, send_from_directory, jsonify
import pandas as pd

from utils.notifier import Notifier
from utils.ibkr_api import IBKRClient
from utils import analysis as anz

with open("config.json", "r", encoding="utf-8") as f:
    CFG = json.load(f)

app = Flask(__name__, static_folder="dashboard/static", static_url_path="/static")

notifier = Notifier(CFG)
ib = IBKRClient()

running = False
last_signals = []

def read_signals():
    path = CFG["paths"]["signals_csv"]
    if not os.path.exists(path):
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        return df
    except:
        return pd.DataFrame()

def worker_loop():
    global running, last_signals
    poll = max(1, int(CFG.get("poll_secs",5)))
    while running:
        df = read_signals()
        batch_msgs = []
        for _, row in df.iterrows():
            t = str(row.get("type","")).lower()
            sym = str(row.get("symbol","")).upper()
            if t in ("","equity","stock") and CFG["analysis"]["equities"]:
                res = anz.analyze_equity(sym, CFG)
                if res.get("ok"):
                    msg = f"📢 سهم {sym} | إشارة: {res['signal']} | RSI={res['rsi']:.1f}"
                    batch_msgs.append(msg)
            elif t in ("spxw","option","spx") and CFG["analysis"]["spxw"]:
                if anz.spxw_filter(row, CFG):
                    side = str(row.get("side","")).upper()
                    msg = f"📢 SPXW | {side} | {row.get('symbol','SPX')} | Δ={row.get('delta','?')} | K={row.get('strike','?')} | Exp={row.get('expiry','?')}"
                    batch_msgs.append(msg)
        # ارسل مرة واحدة
        for m in batch_msgs:
            notifier.send(m)
        last_signals = batch_msgs
        time.sleep(poll)

@app.route("/")
def home():
    return send_from_directory("dashboard", "dashboard.html")

@app.route("/api/ping")
def api_ping():
    ok = ib.connect()
    return jsonify({"ok": bool(ok), "message": "اتصال IBKR ناجح ✅" if ok else "فشل الاتصال بـ IBKR ❌"})

@app.route("/api/start")
def api_start():
    global running
    if running:
        return jsonify({"message":"الفحص يعمل بالفعل"})
    running = True
    threading.Thread(target=worker_loop, daemon=True).start()
    return jsonify({"message":"تم بدء الفحص التلقائي", "signals": last_signals})

@app.route("/api/stop")
def api_stop():
    global running
    running = False
    return jsonify({"message":"تم إيقاف الفحص"})

if __name__ == "_main_":
    app.run(host="127.0.0.1", port=7860, debug=False, threaded=False)
