from email.policy import default
import random
import time
import hashlib
import json

class Block:

    def __init__(self, index, previous_hash, transaction) -> None:
        """ Create A Genesis Block"""
        self.index = index + 1
        self.previous_hash = previous_hash
        self.timestamp = time.asctime(time.localtime(time.time()))
        self.transaction = transaction
        self.nonce = random.randint(1,10)
        self.hash = self.get_hash()

    def get_hash(self):
        """ Calculate hash value of a block.
            Return: hash value 
        """
        data = str(self.index) + self.timestamp + self.transaction + self.previous_hash + str(self.nonce)
        hash256 = hashlib.sha256()
        hash256.update(data.encode('utf-8')) # way of encode
        return hash256.hexdigest()

    def mine_block(self, difficulty):
        """ Proof of Work: Prove we have spent a lof of computing power
            in making a block. 
            The computing speed depends on difficulty of puzzle.
        """
        target_hash = '0' * difficulty
        while self.hash[:difficulty] != target_hash:
            self.nonce += random.randint(1,10)
            self.hash = self.get_hash()
            #print('Try hash -> ' + self.hash) #check all possible hash that we have tried.
        print('-----Mining Done!-----')


class SimpleChain:
    def __init__(self, difficulty) -> None:
        self.chain = []
        self.difficulty = difficulty

    def add_block(self, block):
        block.mine_block(self.difficulty)
        self.chain.append(block)

    def show_all_block(self):
        json_out = json.dumps(self.chain, default=self.get_block_dict)#self.get_block_dict works as bound method
        print(json_out)
    
    def get_block_dict(self, block):
        return block.__dict__

    def is_valid(self):
        for index, block in enumerate(self.chain):
            if index == 0:
                continue
            cur_block = block
            previous_block = self.chain[index - 1]
            if cur_block.hash != cur_block.get_hash():
                print('Current Block is unvalid!')
                return False
            if cur_block.previous_hash != previous_block.hash:
                print('Previous Block been forged!')
                return False
            print('-----All the blocks are valid-----')
            return True

simplechain = SimpleChain(difficulty=4)
simplechain.add_block(Block(0, '0000000', 'I am a genesis block'))
simplechain.add_block(Block(1, simplechain.chain[-1].hash, 'I am the second block'))
simplechain.show_all_block()
simplechain.is_valid()



