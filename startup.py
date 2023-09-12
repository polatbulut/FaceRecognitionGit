import main


class Start:
    def __init__(self):
        self.camera_count = main.count_connected_cameras()
        print(f"{self.camera_count} cameras connected")

    @staticmethod
    def open_app():
        app = main.Main()
        app.load_images()


if __name__ == '__main__':
    start = Start()
    start.open_app()
