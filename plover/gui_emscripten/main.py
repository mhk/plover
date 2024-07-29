# old
# from threading import Event
# from plover.oslayer.keyboardcontrol import KeyboardEmulation
from plover.gui_emscripten.engine import Engine

def show_error(title, message):
    print('%s: %s' % (title, message))

# def main(config, controller):
#     engine = Engine(config, controller, KeyboardEmulation())
#     if not engine.load_config():
#         return 3
#     quitting = Event()
#     engine.hook_connect('quit', quitting.set)
#     engine.start()
#     try:
#         quitting.wait()
#     except KeyboardInterrupt:
#         engine.quit()
#     return engine.join()

# NEW
from plover.config import Config, DictionaryConfig
from plover.gui_emscripten.add_translation import AddTranslation
from plover.oslayer.keyboardcontrol import KeyboardEmulation


class FakeKeyboardEmulation:
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

class FakeController:

    def send_command(self, command):
        pass

    def start(self, message_cb):
        pass

    def stop(self):
        pass

def main2():
    from plover.registry import registry
    registry.update()
    main(None, None)

def setDictionary(engine, path='main.json'):
    dictionaries = [DictionaryConfig.from_dict({'path': path, 'enabled': True})]
    engine.config = { 'dictionaries': dictionaries }

def main(config, controller):
    config = Config('./plover.cfg')
    engine = Engine(config, controller, KeyboardEmulation())
    if not engine.load_config():
        return 3
    engine.start()
    try:
        import js
        from pyodide.ffi import create_proxy
        setDict = lambda path: setDictionary(engine, path)
        js.createObject(create_proxy(setDict), "pyCallback_set_dictionary")
    except ImportError:
        pass
    try:
        return engine.run()
    except KeyboardInterrupt:
        engine.quit()
        engine.run()
    return engine.join()


