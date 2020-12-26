# list.py
#
# Copyright 2020 brombinmirko <send@mirko.pm>
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

@Gtk.Template(resource_path='/pm/mirko/maui-store/list-entry.ui')
class MauiStoreListEntry(Gtk.Box):
    __gtype_name__ = 'MauiStoreListEntry'

    img_package = Gtk.Template.Child()
    package_name = Gtk.Template.Child()
    package_description = Gtk.Template.Child()
    btn_install = Gtk.Template.Child()

    def __init__(self, window, package, **kwargs):
        super().__init__(**kwargs)

        '''
        Initialize template
        '''
        self.init_template()

        '''
        Common variables
        '''
        self.window = window
        self.repository = window.repository

        '''
        Populate widgets with data
        '''
        self.package_name.set_text(package.get("name"))

@Gtk.Template(resource_path='/pm/mirko/maui-store/list.ui')
class MauiStoreList(Gtk.Box):
    __gtype_name__ = 'MauiStoreList'

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

        '''
        Initialize template
        '''
        self.init_template()

        '''
        Common variables
        '''
        self.window = window
        self.repository = window.repository

        for package in self.repository.list_packages():
            self.add(MauiStoreListEntry(self.window, package))
