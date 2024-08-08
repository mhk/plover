from plover.oslayer.keyboardcontrol import KeyboardEmulation

from plover.gui_emscripten.engine import Engine

from plover.config import DictionaryConfig


def show_error(title, message):
    print('%s: %s' % (title, message))

def setDictionary(engine, path='main.json'):
    dictionaries = [DictionaryConfig.from_dict({'path': path, 'enabled': True})]
    engine.config = { 'dictionaries': dictionaries }

def main(config, controller):
    engine = Engine(config, controller, KeyboardEmulation())
    if not engine.load_config():
        return 3
    engine.start()
    # return engine
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


