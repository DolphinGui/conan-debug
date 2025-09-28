from conan import ConanFile
from conan.tools.files import get
from os.path import join
import os

class JimTCL(ConanFile):
    name = "jimtcl"
    version = "0.83"
    description = "jimTCL packaged for Conan"
    license = "BSD-2"
    homepage = "https://jim.tcl.tk/home/doc/www/www/index.html"
    generators = "VirtualBuildEnv"

    def requirements(self):
        pass

    def build_requirements(self):
        pass

    def generate(self):
        configure = join(self.source_folder, "configure")
        cmd = str(configure) + f" --prefix={self.package_folder}"
        self.run(cmd, shell=True)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        self.run(f"make -j -l {os.process_cpu_count()}")

    def package(self):
        self.run(f"make -j -l {os.process_cpu_count()} install", cwd=self.source_folder)
