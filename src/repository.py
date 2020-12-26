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

logging.basicConfig(level=logging.DEBUG)

class MauiStoreRepository:

    repository_base_url = "https://raw.githubusercontent.com/AppImage/appimage.github.io/master/database/"
    repository_index = "https://appimage.github.io/search.json"
    repository_package = repository_base_url + "%s/package.json"
    repository_local = "%s/.local/MauiStore" % Path.home()
    repository_local_index = "%s/repository.json" % repository_local
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

                '''
                Fix missing items in package
                '''
                if "license" not in package:
                    package["license"] = "Undefined"
                if "author" not in package:
                    package["license"] = "Undefined"
                if "license" not in package:
                    package["license"] = "Undefined"
                if "description" not in package:
                    package["license"] = "No description provided."

                return package
        except:
            logging.warning("No valid manifest found for `%s`" % name)
            return False

    '''
    Fetch packages first from local repository or online if missing cache
    '''
    def fetch_packages(self):
        cache_packages = []

        try:
            local_repository = open(self.repository_local_index)
            cache_packages = json.load(local_repository)
            local_repository.close()
            local=True
            logging.info("Local repository found.")
        except:
            logging.info("No local repository found, fetching from online ..")
            local=False
            with urllib.request.urlopen(self.repository_index) as url:
                packages = json.loads(url.read().decode("utf-8"))

            '''
            TODO: remove filter  0:3
            '''
            for package in packages[0:3]:
                package_data = self.get_package(package.get("title"))

                if package_data:
                    new_package = {
                        "name": package_data["name"],
                        "version": package_data["version"],
                        "license": package_data["license"],
                        "description": package_data["description"],
                        "author": package_data["author"],
                        "homepage": "",
                        "icon": "",
                        "screenshot": ""
                    }
                    cache_packages.append(new_package)

            logging.info("Caching packages to local repository ..")
            with open(self.repository_local_index, "w") as local_repository:
                json.dump(cache_packages, local_repository, indent=4)
                local_repository.close()

        self.cache_packages = cache_packages


    '''
    List packages with items limit
    '''
    def list_packages(self, items=20):
        return self.cache_packages[0:items]

