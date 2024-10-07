# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: oscserverdecomp.py
# Bytecode version: 3.7.0 (3394)
# Source timestamp: 2024-07-26 23:01:51 UTC (1722034911)

from _osc.RemixNet import OSCServer as Base
from ..ClyphXComponentBase import ClyphXComponentBase, add_client, remove_client

class OSCServer(Base, ClyphXComponentBase):
    """  Note: this uses RemixNet/OSC/struct modules supplied by Nathan Ramella and ST8. '"""

    def __init__(self, refresh_rate=500, receive_only=False, *a, **k):
        Base.__init__(self, *a, **k)
        ClyphXComponentBase.__init__(self)
        self._refresh_rate = refresh_rate
        self._send_dict = {}
        add_client(self)
        if not receive_only:
            pass
        if refresh_rate:
            self._do_recursive_send()

    def disconnect(self):
        ClyphXComponentBase.disconnect(self)
        self._do_shutdown()

    def shutdown(self):
        self._do_shutdown()

    def _do_shutdown(self):
        Base.shutdown(self)
        remove_client(self)
        self._send_dict = None

    def sendOSC(self, address=None, msg=None):
        """ Sends the given message to the given address and caches it. """
        self._send_dict[address] = msg
        Base.sendOSC(self, address, msg)

    def sendOSC_once(self, address=None, msg=None):
        """ Sends the given message without adding to the dictonary and deletes it from the cache"""
        if not self._send_dict.get(address, None) == msg:
            Base.sendOSC(self, address, msg)
        if self._send_dict.get(address):
            self._send_dict.pop(address)
            Base.sendOSC(self, address, msg)

    def refresh(self):
        """ Refreshes/resends all current data. """
        for k, v in self._send_dict.items():
            Base.sendOSC(self, k, v)

    def on_tick(self):
        self.processIncomingUDP()

    def _do_recursive_send(self):
        if self.canonical_parent:
            self.canonical_parent.schedule_message(self._refresh_rate, self._do_recursive_send)