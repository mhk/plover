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
        self.web = False
        if self.web:
            # not used
            import js
            from pyodide.ffi import create_proxy
            js.createObject(create_proxy(self.pyKeyDown), "pyCallback_key_down")
            js.createObject(create_proxy(self.pyKeyUp)  , "pyCallback_key_up")
            self.start = self.web_start
            self.cancel = self.web_cancel
            self.suppress_keyboard = self.web_suppress
        else:
            import threading
            self._thread = threading.Thread(name='KeyboardCapture', target=self._run)
            self._cancelled = False
            self.start = self.thread_start
            self.cancel = self.thread_cancel
            self.suppress_keyboard = self.thread_suppress

    def pyKeyDown(self, key):
        print(f"pyKeyDown: {key}")
        self.key_down(key);

    def pyKeyUp(self, key):
        print(f"pyKeyUp: {key}")
        self.key_up(key);

    def web_start(self):
        pass

    def cancel(self):
        pass

    def suppress(self, suppressed_keys=()):
        pass

    def _handler(self, key_events):
        for evt in key_events.strip().split():
            if evt.strip().lower() == 'quit' or evt.strip().lower() == 'exit':
                return False
            if evt.startswith('+'):
                self.key_down(evt[1:])
            elif evt.startswith('-'):
                self.key_up(evt[1:])
            else:
                self.key_down(evt)
                self.key_up(evt)
        return True

    def _run(self):
        finished = False
        while not (finished or self._cancelled):
            key_events = input('--> ');
            finished = not self._handler(key_events)

    def thread_start(self):
        self._thread.start()

    def thread_cancel(self):
        self._cancelled = True

    def thread_suppress(self, suppressed_keys=()):
        pass
