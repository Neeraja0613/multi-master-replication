from app.replication import update_product
import threading

def us():
    update_product("us", "11111111-1111-1111-1111-111111111111", 100)

def eu():
    update_product("eu", "11111111-1111-1111-1111-111111111111", 105)

t1 = threading.Thread(target=us)
t2 = threading.Thread(target=eu)

t1.start()
t2.start()

t1.join()
t2.join()