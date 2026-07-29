class Node:
    def __init__(self,char=None,freq=0):
        self.char=char
        self.freq=freq
        self.left=None
        self.right=None
    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq< other.freq
        return self.char < other.char
