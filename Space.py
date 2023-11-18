class Space():
    def __init__(self, x: int, y: int, val: int = 0):
        self.x = x
        self.y = y
        self.val = val
        self.color = (255, 255, 255)
        self.rect = None
        self.rectx = None
        self.recty = None
        self.width = None
        self.height = None

        self.failed_values = []