from conan import ConanFile
from conan.tools.files import copy, download, rm, rmdir
import os

class OpenOCDWin(ConanFile):
    name = "openocd-win"
    version = "20250710"
    description = "OpenOCD built for windows"
    license = "GPL-2.0-or-later"
    homepage = "https://gnutoolchains.com/arm-eabi/openocd/"

    def requirements(self):
        pass

    def build_requirements(self):
        self.tool_requires("7zip/25.00")
        pass

    def generate(self):
        download(self, filename="openocd.7z", **self.conan_data["sources"]["v" + str(self.version)])

    def build(self):
        self.run("7z.exe x openocd.7z")
        rm(self, "openocd.7z", self.build_folder)

    def package(self):
        dirname = self.conan_data["data"]["v" + str(self.version)]["dirname"]
        copy(self, "*/*", src=os.path.join(self.build_folder, dirname), dst=self.package_folder)
