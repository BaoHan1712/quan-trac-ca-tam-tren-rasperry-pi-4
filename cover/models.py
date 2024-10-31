import threading

class Threading:
    def __init__(self):
        self.run = None

    def start(self, target, **kwargs):
        self.run = threading.Thread(
            target=target,
            kwargs=kwargs,
            daemon=True,
        )
        self.run.start()

    def stop(self):
        self.run.join()

    def is_alive(self):
        return self.run.is_alive()