from plover.machine.keyboard_capture import Capture

class KeyboardEmulation:
    def __init__(self):
        self.text = ''
        try:
            import js
            from pyodide.ffi import create_proxy
            js.createObject(create_proxy(self.reset_text), "pyCallback_reset_text")
        except ImportError:
            pass

    def reset_text(self):
        self.text = ''

    def _update_text(self, text, s):
        try:
            import js
            js.jsCallback_update_text(text, s)
        except ImportError:
            print(s)

    def send_backspaces(self, count):
        self.text = self.text[:-count]
        self._update_text(self.text, f"")

    def send_string(self, s):
        self.text += s
        self._update_text(self.text, s)

    def send_key_combination(self, combo):
        print(combo)


class KeyboardCapture(Capture):
    def __init__(self):
        self.keys_pressed = set()
        try:
            import js
            from pyodide.ffi import create_proxy
            js.createObject(create_proxy(self.pyKeyDown), "pyCallback_key_down")
            js.createObject(create_proxy(self.pyKeyUp)  , "pyCallback_key_up")
            self.start = self.web_start
            self.cancel = self.web_cancel
            self.suppressd = self.web_suppress
            self.run = self.web_run
        except ImportError:
            self._cancelled = False
            self.start = self.web_start
            self.cancel = self.thread_cancel
            self.suppress = self.thread_suppress
            self.start = self.thread_start
            self.run = self.thread_run

    def _console(self, text):
        try:
            import js
            js.console.log(text)
        except ImportError:
            pass

    def pyKeyDown(self, key):
        self.keys_pressed.add(key)
        self._console(f"pyKeyDown '{key}' [{' '.join(self.keys_pressed)}]")
        self.key_down(key);

    def pyKeyUp(self, key):
        self.keys_pressed.remove(key)
        self._console(f"pyKeyUp '{key}' [{' '.join(self.keys_pressed)}]")
        self.key_up(key);

    def web_start(self):
        pass

    def web_run(self):
        pass

    def web_cancel(self):
        pass

    def web_suppress(self, suppressed_keys=()):
        pass

    def _handler(self, key_events):
        for evt in key_events.strip().split():
            if evt.strip().lower() == 'quit' or evt.strip().lower() == 'exit':
                return False
            if evt.startswith('+'):
                for e in evt[1:]:
                    self.key_down(e)
            elif evt.startswith('-'):
                for e in evt[1:]:
                    self.key_up(e)
            else:
                for e in evt:
                    self.key_down(e)
                for e in evt:
                    self.key_up(e)
        return True

    def thread_run(self):
        finished = False
        while not (finished or self._cancelled):
            try:
                key_events = input('--> ');
                finished = not self._handler(key_events)
            except EOFError:
                finished = True

    def thread_start(self):
        pass

    def thread_cancel(self):
        self._cancelled = True

    def thread_suppress(self, suppressed_keys=()):
        pass
