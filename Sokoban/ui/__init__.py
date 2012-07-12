class UI(object):
    def __init__(self, main, parent):
        self.main = main
        self.parent = parent

    def handle_key(self, event):
        pass

    def handle_key_up(self, event):
        pass

    def handle_click(self, event):
        pass

    def handle_click_up(self, event):
        pass

    def handle_drag(self, event):
        self.handle_motion(event)

    def handle_scroll(self, event):
        pass

    def handle_motion(self, event):
        pass

    def reblit(self, surf):
        pass

    def on_reentry(self, child):
        pass

    def print_ui_stack(self):
        x = self
        while x:
            print x.__class__
            x = x.parent