from pypresence import Presence
import os

class RichPresence:
    def __init__(self, client_id):
        self.presence = Presence(client_id=client_id)
        self.connected = False

    def connect(self):
        self.presence.connect()

    def update(self, state, large_text=None, details=None, party_size=None, party_id=None, join=None):
        try:
            if party_size != None:
                self.presence.update(
                    state=state,
                    large_image = "main_logo",
                    large_text = large_text,
                    party_size=party_size,
                    party_id=party_id,
                    join=join,
                    pid=os.getpid()
                )
            else:
                self.presence.update(
                    state=state,
                    large_image = "main_logo",
                    large_text = large_text,
                    pid=os.getpid(),
                )
        except Exception as exception:
            print(exception)
            self.connected = False

# updatePresence(party_size=[1,2], party_id="testid", join="testjoin")