from pypresence import Presence
import os
import time

client_id = '825326652124430366'
RPC = Presence(client_id=client_id)

try:
    c = RPC.connect()
except:
    print("RPC connection failed. Maybe discord is not running")

lock_status = False

def updatePresence(details="Idle", state="En développement", party_size=None, party_id=None, join=None):
    if party_size != None:
        test = RPC.update(
            state=state,
            large_image="main_logo",
            large_text ="Ouais le nom est pas ouf mais en vrai ça passe",
            party_size=party_size,
            party_id="52525252",
            join="a43aze5az4e5za4e52",
            pid=os.getpid()
        )
        print(test)
    else:
        RPC.update(
            state=state,
            large_image="main_logo",
            large_text ="Ouais le nom est pas ouf mais en vrai ça passe",
            pid=os.getpid(),
        )

while True:
    updatePresence(party_size=[1,2], party_id="testid", join="testjoin")
    time.sleep(5)

input("test")

# details=f"Loot : ${loot} | Cut : ${cut}",