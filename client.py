# https://github.com/sushi-irc/nigiri

import urwid
import sys
import extends
from extends import *
from urwid import MetaSignals

class ClientWindow(object):

    __metaclass__ = MetaSignals
    signals = ["quit", "keypress", "tab_switched"]

    _palette = [
            ('divider', '', '', '', '#fff', '#2c5'),
            ('text', 'light gray', 'default'),
            ('bold_text', 'light gray', 'default', 'bold'),
            ('warning_text', '', '', '', '#e1d', '#fff'),
            ('pending_text', '', '', '', '#bbb', '#fff'),
            ('confirmed_text', '', '', '', '#1df', '#fff'),
            ("body", "text"),
            ("footer", "text"),
            ("header", "text"),
        ]

    for type, bg in (
            ("div_fg_", "dark cyan"),
            ("", "default")):
        for name, color in (
                ("red", "dark red"),
                ("blue", "dark blue"),
                ("green", "dark green"),
                ("yellow", "yellow"),
                ("magenta", "dark magenta"),
                ("gray", "light gray"),
                ("white", "white"),
                ("black", "black")):
            _palette.append((type + name, color, bg))


    def __init__(self, block_chain, peers, msgq):
        self.shall_quit = False
        self.block_chain = block_chain
        self.peers = peers
        self.msgq = msgq


    def start(self):
        """ entry point to start UI """
        self.ui = urwid.raw_display.Screen()
        self.ui.set_terminal_properties(colors=256)
        self.ui.register_palette(self._palette)
        self.build_interface()

        self.ui.run_wrapper(self.run)


    def run(self):
        """ setup input handler, invalidate handler to
            automatically redraw the interface if needed.
            connect to dbus, start mainloop.
        """

        def input_cb(key):
            if self.shall_quit:
                raise urwid.ExitMainLoop
            self.keypress(self.size, key)

        self.size = self.ui.get_cols_rows()

        self.main_loop = urwid.MainLoop(
            self.context,
            screen=self.ui,
            handle_mouse=False,
            unhandled_input=input_cb,
        )

        def call_redraw(*x):
            self.draw_interface()
            invalidate.locked = False
            return True

        inv = urwid.canvas.CanvasCache.invalidate

        def invalidate (cls, *a, **k):
            inv(*a, **k)

            if not invalidate.locked:
                invalidate.locked = True
                self.main_loop.set_alarm_in(0, call_redraw)

        invalidate.locked = False
        urwid.canvas.CanvasCache.invalidate = classmethod(invalidate)

        try:
            self.main_loop.run()
        except KeyboardInterrupt:
            self.quit()

    def quit(self, _exit=True):
        """ stops the ui, exits the application (if exit=True)
            After the UI is stopped, the config is written.
        """
        urwid.emit_signal(self, "quit")
        self.shall_quit = True
        if _exit:
            sys.exit(0)

    def _create_widgets(self):
        """ create the UI widgets """
        self.header = urwid.Text(" SHOUT ", align="center")
        self.footer = extends.Edit.ExtendedEdit("> ")
        self.divider = urwid.Text(" Shout your message: ")

        self.generic_output_walker = urwid.SimpleListWalker([])
        self.body = extends.ListBox.ExtendedListBox(self.generic_output_walker)

        urwid.connect_signal(self.body, "set_auto_scroll", self.handle_body_auto_scroll)

    def _setup_widgets(self):
        """ set coloring and attributes of the UI widgets
            created in _create_widgets
        """
        self.header = urwid.AttrWrap(self.header, "divider")
        self.footer = urwid.AttrWrap(self.footer, "footer")
        self.divider = urwid.AttrWrap(self.divider, "divider")
        self.body = urwid.AttrWrap(self.body, "body")

        self.footer.set_wrap_mode("space")

    def _setup_context(self):
        """ wrap a Frame called context around the widgets
            created in _create_widgets
        """
        self.context = urwid.Frame(self.body, header=self.header, footer=self.divider)
        self.context = urwid.Frame(self.context, footer=self.footer)
        self.context.set_focus("footer")

    def build_interface(self):
        """ call the widget methods to build the UI """
        self._create_widgets()
        self._setup_widgets()
        self._setup_context()

    def draw_interface(self):
        self.main_loop.draw_screen()

    def keypress(self, size, key):
        """ handle keypress events """

        urwid.emit_signal(self, "keypress", size, key)

        if key == "window resize":
            self.size = self.ui.get_cols_rows()

        elif key == "enter":
            text = self.footer.get_edit_text()
            self.footer.set_edit_text(" "*len(text))
            self.footer.set_edit_text("")

            self.print_text(text, "pending_text")
            self.msgq.add_message(text)



        elif key == "up":

            w = self.generic_output_walker
            prev = w.get_prev(w.get_focus()[1])[1]
            if prev is not None:
                w.set_focus(prev)

            # self.body.keypress(size, key)

        elif key == "ctrl b":
            self.print_text(str(self.block_chain), "confirmed_text")

        elif key == "ctrl p":
            self.print_text(str(self.peers), "confirmed_text")


        elif key == "down":
            w = self.generic_output_walker
            next = w.get_next(w.get_focus()[1])[1]
            if next is not None:
                w.set_focus(next)


        elif key == "ctrl u":
            # clear the edit line
            self.footer.set_edit_text ("")
            self.footer.set_edit_pos (0)

        elif key == "ctrl w":
            # remove the text from cursor
            # position to previous space

            def ctrlw(et, ep):
                i = et[:ep].rfind(" ")
                if i == -1:
                    et = et[ep:]
                else:
                    et = et[:i+1] + et[ep:]
                return et

            # FIXME: fix position setting
            new = ctrlw(
                self.footer.get_edit_text(),
                self.footer.edit_pos)
            self.footer.set_edit_text(new)

        else:
            self.context.keypress(size, key)


    def print_text(self, text, format="confirmed_text"):
        """print the given text in the _current_ window"""

        walker = self.generic_output_walker

        if text and text[-1] == "\n":
            text = text[:-1]

        walker.append(urwid.Text((format, text)))

        walker.set_focus(len(walker) - 1)
        self.draw_interface()

# Signal handlers

    def handle_body_auto_scroll(self, auto_scroll):
        self.body.auto_scroll = auto_scroll


# if __name__ == "__main__":
#     global main_window, stderr
#     window = ClientWindow()
#     # sys.excepthook = except_hook
#     # signals.setup(window)
#     # messages.setup(window)
#     # tabcompletion.setup(window)
#
#     window.start()