# window.py
#
# Copyright 2020 Mirko Brombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk


@Gtk.Template(resource_path='/pm/mirko/maui-store/window.ui')
class MauiStoreWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MauiStoreWindow'

    btn_back = Gtk.Template.Child()
    btn_refresh = Gtk.Template.Child()
    btn_installed = Gtk.Template.Child()
    btn_translate = Gtk.Template.Child()
    btn_support = Gtk.Template.Child()
    btn_preferences = Gtk.Template.Child()
    btn_about = Gtk.Template.Child()
    switch_dark = Gtk.Template.Child()
    stack_main = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        '''
        Initialize template
        '''
        self.init_template()
