import app
import scene
from scene_today import SceneToday


def main():
    app.init()
    scene.push(SceneToday())
    app.run()
    app.quit()


if __name__ == "__main__":
    main()
