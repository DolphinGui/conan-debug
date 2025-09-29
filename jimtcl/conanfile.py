from conan import ConanFile
from conan.tools.files import get, replace_in_file, load, save
from os.path import join
from io import StringIO
from conan.tools.env import VirtualBuildEnv
import os
import re

class JimTCL(ConanFile):
    name = "jimtcl"
    version = "0.83"
    description = "jimTCL packaged for Conan"
    license = "BSD-2"
    homepage = "https://jim.tcl.tk/home/doc/www/www/index.html"
    settings = "os", "compiler", "build_type", "arch"
    generators = "VirtualBuildEnv"
    win_bash = True

    def requirements(self):
        self.tool_requires("tcl/8.6.13")
        if self.settings.os == "Windows":
            self.tool_requires("msys2/cci.latest")

    def build_requirements(self):
        pass

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        #replace_in_file(self, join(self.source_folder, "autosetup", "autosetup-find-tclsh"), "tclsh8.6", "tcl86tsx.exe")

    def fix_path(self, path):
        if self.settings.os != "Windows":
            return path
        out = StringIO()
        self.run(f"cygpath -u '{path}'", shell=True, stdout=out)
        out = out.getvalue()
        return out.splitlines()[-1] # msys2 is weird on conan and outputs extraneous stuff. Discard it. 

    def generate(self):
        env = VirtualBuildEnv(self).environment()
        env.define("autosetup_tclsh", "tclsh86tsx.exe")
        envvars = env.vars(self, "build")
        envvars.save_script("conan_environment.sh")
        configure = self.fix_path(join(self.source_folder, "configure"))
        args = ""
        if self.settings.os == "Windows":
            args = "--with-ext='win32'"
        cmd = ("source ./conan_environment.sh && "
             + str(configure) + f" --disable-docs --prefix={self.fix_path(self.package_folder)} {args}")
        self.run(cmd, shell=True)
        makefile_path = join(self.build_folder, "Makefile")
        makefile = load(self, makefile_path)
        makefile = re.sub(r'\$\(INSTALL_DATA\) +build-jim-ext.+\n', "", makefile)
        save(self, makefile_path, makefile) 

    def build(self):
        self.run("cat Makefile")
        self.run(f"make -j -l {os.process_cpu_count()}")

    def package(self):
        self.run(f"make -j -l {os.process_cpu_count()} install", cwd=self.source_folder)
