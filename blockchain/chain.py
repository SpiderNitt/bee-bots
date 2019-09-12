from block import Block
import datetime
import copy


class BlockChain:
    def __init__(self):
        self.blocks = [self.get_genesis_block()]

    def get_genesis_block(self):
        return Block(0, datetime.datetime.utcnow(), "Genesis", "arbitrary")

    def fork(self):
        c = copy.deepcopy(self)
        c.blocks = c.blocks[0 : len(self.blocks)]
        return c

    def add_block(self, data):
        chain2 = self.fork()

        block = Block(
            len(self.blocks),
            datetime.datetime.utcnow(),
            data,
            self.blocks[len(self.blocks) - 1].hash,
        )
        if block.pow == -1:
            print("proof of work timed out. block wont be inserted. bye bye")
        else:
            self.blocks.append(block)
            flag = self.verify()
            if not flag:
                print("thiere is a conflict with the block. aborting!!!")
                self.blocks = self.blocks[0 : len(self.blocks - 1)]

            else:
                # print("this is the correct length: ", len(self.blocks))

                print("Block with index " + str(len(self.blocks)) + " added")

    def verify(self):
        flag = True
        for i in range(1, len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False

            if self.blocks[i - 1].hash != self.blocks[i].previous_hash:
                flag = False

            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False

            if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                flag = False
        return flag


chain = BlockChain()
chain.add_block("356")



print("length of chain? ", len(chain.blocks))
print(chain.blocks[len(chain.blocks) - 1].hash)
