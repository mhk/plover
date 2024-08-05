class Controller:
    def is_owner(self):
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def send_command(self, command):
        pass

    def start(self, message_cb):
        pass

    def stop(self):
        pass
