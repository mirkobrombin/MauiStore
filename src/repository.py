# repository.py
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

import os, logging, urllib.request, json

from pathlib import Path

class MauiStoreRepository:

    repository_base_url = "https://raw.githubusercontent.com/AppImage/appimage.github.io/master/database/"
    repository_index = "https://appimage.github.io/search.json"
    repository_package = repository_base_url + "%s/package.json"
    repository_local = "%s/.local/MauiStore" % Path.home()
    repository_local_index = "%s/repository.json" % repository_local
    package = {
        "name": "",
        "productName": "",
        "version": "",
        "license": "",
        "description": "",
        "author": {
            "name": "",
            "email": "",
            "url": ""
        },
        "homepage": "",
        "icon": "",
        "screenshot": ""
    }
    cache_packages = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.check_directories()
        self.fetch_packages()

    '''
    Check for essentials directories then create if missing
    '''
    def check_directories(self):
        try:
            if not os.path.isdir(self.repository_local):
                logging.warning("Repository path doens't exist, creating now.")
                os.makedirs(self.repository_local, exist_ok=True)
        except:
            logging.warning("Path cannot be created.")
            return False

    '''
    Get package data from online repository
    '''
    def get_package(self, name):
        try:
            with urllib.request.urlopen(self.repository_package % name) as url:
                package = json.loads(url.read().decode("utf-8"))

                return package
        except:
            logging.warning("No valid manifest found for `%s`" % name)
            return False

    def fetch_packages(self):
        cache_packages = []

        try:
            local_repository = open(self.repository_local_index)
            packages = json.load(local_repository)
            local_repository.close()
        except:
            with urllib.request.urlopen(self.repository_index) as url:
                packages = json.loads(url.read().decode("utf-8"))

        '''
        TODO: remove filter 0:20
        '''
        for package in packages[0:20]:
            package_data = self.get_package(package.get("title"))

            if package_data:
                new_package = self.package
                if "name" in package_data:
                    new_package["name"] = package_data["name"]
                if "description" in package_data:
                    new_package["description"] = package_data["description"]
                if "version" in package_data:
                    new_package["version"] = package_data["version"]
                if "license" in package_data:
                    new_package["license"] = package_data["license"]
                if "author" in package_data:
                    new_package["author"] = package_data["author"]

                cache_packages.append(new_package)

        self.cache_packages = cache_packages

        '''
        Cache packages to local repository
        '''
        with open(self.repository_local_index, "w") as local_repository:
            json.dump(cache_packages, local_repository, indent=4)
            local_repository.close()


    def list_packages(self, items=20):
        return self.cache_packages[0:items]

