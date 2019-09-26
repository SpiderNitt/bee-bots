import hashlib
import threading


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.is_timed_out = False
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        if index == 0:
            self.pow = 0
        else:
            self.pow = self.proof_of_work()
        self.hash = self.hashing()

    def mytimer(self, time_limit=10.0):
        self.is_timed_out = True

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode("utf-8"))
        key.update(str(self.timestamp).encode("utf-8"))
        key.update(str(self.data).encode("utf-8"))
        key.update(str(self.previous_hash).encode("utf-8"))
        key.update(str(self.pow).encode("utf-8"))
        return key.hexdigest()

    def proof_of_work(self, puzzle_bits=4, time_limit=10.0):
        my_timer = threading.Timer(time_limit, self.mytimer)
        my_timer.start()
        for i in range(pow(2, 256)):
            if not self.is_timed_out:
                m = hashlib.sha256()
                m.update(str(self.index).encode("utf-8"))
                m.update(str(self.timestamp).encode("utf-8"))
                m.update(str(self.data).encode("utf-8"))
                m.update(str(self.previous_hash).encode("utf-8"))
                m.update(str(i).encode("utf-8"))
                string = m.hexdigest()
                if string[0:1] == "0":
                    print("hit hit hit for", i)
                    my_timer.cancel()
                    return i

            else:
                print("timed out. -1 returned")
                return -1

