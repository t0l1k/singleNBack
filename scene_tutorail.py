import conf


class SceneTutorial:
    def __init__(self, app) -> None:
        self.app = app
        self.next = None

    def getScene(self):
        return self.next

    def setScene(self, next):
        self.next = next

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(conf.gray)

    def keyPressed(self):
        self.app.setSceneToday()

    def quit(self):
        return False
