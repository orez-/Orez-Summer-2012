class TacticsUI(object):
    def __init__(self, main, parent=None):
        self.main = main
        self.parent = parent

    def redraw(self):
        pass

    def reblit(self, screen):
        pass

    def keydown(self, event):
        pass

    def keyup(self, event):
        pass

    def keep_moving(self):
        """ Called every frame: should probably be renamed. """
        pass

    def k_UP(self):
        """ Called when the user presses a key marked as 'up' """
        pass

    def k_DOWN(self):
        """ Called when the user presses a key marked as 'down' """
        pass

    def k_LEFT(self):
        """ Called when the user presses a key marked as 'left' """
        pass

    def k_RIGHT(self):
        """ Called when the user presses a key marked as 'right' """
        pass

    def k_CANCEL(self):
        pass

    def k_OK(self):
        pass

    def k_PAUSE(self):
        pass

    @staticmethod
    def name():
        print "uh"
        #raise NotImplementedError