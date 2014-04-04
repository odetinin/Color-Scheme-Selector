import sublime, sublime_plugin
import os

class SelectColorSchemeCommand(sublime_plugin.WindowCommand):

    def run(self):
        global previous_scheme_index

        if int(sublime.version()) > 3000:
            color_schemes = sublime.find_resources("*.tmTheme")
        else:
            print("This plugin is designed to work in Sublime Text 3 only.")
            return

        black_list = sublime.load_settings('ColorSchemeSelector.sublime-settings').get('black_list')
        if black_list == None:
            black_list = []
        black_list.append('/InactivePanes/')
        black_list.append('(SL).tmTheme')

        for item in black_list:
            color_schemes = [color_scheme for color_scheme in color_schemes if item not in color_scheme]

        current_scheme_index = self.current_scheme_index(color_schemes)
        previous_scheme_index = -1

        def on_done(index):
            self.set_color_scheme(color_schemes[index])

        def on_change(index):
            global previous_scheme_index

            if previous_scheme_index == -1:
                previous_scheme_index = index
                return

            self.set_color_scheme(color_schemes[index])

            try:
                os.remove(sublime.packages_path() + '/User/' + os.path.basename(color_schemes[previous_scheme_index]).replace('.tmTheme', '') + ' (SL).tmTheme')
            except:
                pass
            previous_scheme_index = index

        items = [[os.path.basename(_), _] for _ in color_schemes]
        self.window.show_quick_panel(items, on_done, 0, current_scheme_index, on_change)

    def current_scheme_index(self, color_schemes):
        current_scheme = self.load_settings().get('color_scheme').replace(' (SL)', '')
        try:
            index = [c for c in color_schemes].index(current_scheme)
        except:
            index = [os.path.basename(c) for c in color_schemes].index(os.path.basename(current_scheme))
        return index

    def set_color_scheme(self, color_scheme_path):
        self.load_settings().set('color_scheme', color_scheme_path)
        sublime.save_settings('Preferences.sublime-settings')
        sublime.status_message('SelectColorScheme: ' + color_scheme_path)

    def load_settings(self):
        return sublime.load_settings('Preferences.sublime-settings')
