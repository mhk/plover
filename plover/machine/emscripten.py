# -*- coding: utf-8 -*-
# Copyright (c) 2010 Joshua Harlan Lifton.
# See LICENSE.txt for details.

"For use with an emscripten keyboard (preferably NKRO) as a steno machine."

from plover import _
from plover.machine.keyboard import Keyboard
from plover.oslayer.keyboardcontrol import KeyboardCapture
from plover.steno import Stroke

# i18n: Machine name.
_._('Emscripten Keyboard')


class EmscriptenKeyboard(Keyboard):
    def start_capture(self):
        """Begin listening for output from the stenotype machine."""
        self._initializing()
        try:
            self._keyboard_capture = KeyboardCapture()
            self._keyboard_capture.key_down = self._key_down
            self._keyboard_capture.key_up = self._key_up
            self._keyboard_capture.start()
            self.run = self._keyboard_capture.run
        except:
            self._error()
            raise
        self._ready()

    def _key_down(self, key):
        super()._key_down(key)
        try:
            import js
            steno_keys = set()
            for k in self._stroke_keys:
                key = self._bindings.get(k)
                if key and key not in steno_keys:
                    js.jsCallback_on(key)
                    steno_keys.add(key)
        except ImportError:
            pass

    def _key_up(self, key):
        steno_keys = super()._key_up(key)
        if None != steno_keys:
            try:
                import js
                stroke = Stroke(steno_keys)
                js.jsCallback_stroke(f"{stroke.rtfcre}")
                for key in steno_keys:
                    js.jsCallback_off(key)
            except ImportError:
                pass
