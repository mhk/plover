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
