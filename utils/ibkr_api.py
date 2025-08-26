# ibkr_api.py
from ib_insync import IB

class IBKRClient:
    def _init_(self, host='127.0.0.1', port=4001, client_id=9, timeout=5):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.timeout = timeout
        self.ib = IB()

    def connect(self) -> bool:
        try:
            if self.ib.isConnected():
                return True
            self.ib.connect(self.host, self.port, clientId=self.client_id, timeout=self.timeout)
            return self.ib.isConnected()
        except Exception as e:
            print(f"IBKR connect error: {e}")
            return False

    def is_connected(self) -> bool:
        return self.ib.isConnected()

    def disconnect(self):
        try:
            if self.ib.isConnected():
                self.ib.disconnect()
        except:
            pass
