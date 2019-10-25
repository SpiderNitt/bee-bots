import hashlib
import threading
import jsonpickle
import numpy as np

stakes = [10, 10, 10, 10, 10]
majority_vote = sum(stakes) / len(stakes)


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.is_timed_out = False
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        if index == 0:
            self.pos = False
        else:
            self.pos = self.proof_of_stake(stakes)
        self.hash = self.hashing()

    def mytimer(self, time_limit=10.0):
        self.is_timed_out = True

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode("utf-8"))
        key.update(str(self.timestamp).encode("utf-8"))
        key.update(str(self.data).encode("utf-8"))
        key.update(str(self.previous_hash).encode("utf-8"))
        key.update(str(self.pos).encode("utf-8"))
        return key.hexdigest()

    # * whether the bot thinks it should update
    def voting(self):
        np.random.shuffle(stakes)
        consesus = 0
        for i in range(0, len(stakes) / 2):
            consesus = consesus + stakes[i]
        if consesus >= majority_vote:
            return True
        else:
            return False

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

    def toJSON(self):
        return jsonpickle.encode(self)
