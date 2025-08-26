# -- coding: utf-8 --
# utils/precheck.py
import socket, sys, requests
from ib_insync import IB

# إعدادات IBKR
host = '127.0.0.1'   # عدل لو تحتاج
port = 4001          # أو 4002 لو على Paper
client_id = 9        # كما طلبت

# ضع هنا بيانات تيليجرام مباشرة:
BOT_TOKEN = "8289640455:AAF7He0c8SeWKjfft0wdWQ7ECKj34y9Hh6A"
CHAT_ID = "8235897299"

def send_tg(msg: str):
    """إرسال رسالة تيليجرام مباشرة باستخدام التوكن والـ chat_id"""
    if BOT_TOKEN and CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        except Exception:
            pass

# 1) فحص TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
try:
    s.connect((host, port))
    s.close()
    tcp_ok = True
except Exception:
    tcp_ok = False

if not tcp_ok:
    send_tg(f"❌ فشل TCP إلى {host}:{port} — تأكد أن IB Gateway يعمل والمنفذ صحيح.")
    sys.exit(1)

# 2) فحص مصافحة API
ib = IB()
try:
    ib.connect(host, port, clientId=client_id)
    api_ok = ib.isConnected()
    ib.disconnect()
except Exception:
    api_ok = False

if not api_ok:
    send_tg(f"❌ المنفذ {port} مفتوح لكن مصافحة API فشلت (ClientId={client_id}). راجع API/Trusted IPs/ClientId.")
    sys.exit(1)

# إذا نجح الاتصال
send_tg(f"✅ اتصال IBKR ناجح — {host}:{port} (ClientId={client_id}). سيتم تشغيل البوت الآن.")
sys.exit(0)