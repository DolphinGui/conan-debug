from conan import ConanFile
from conan.tools.gnu import AutotoolsToolchain, Autotools, AutotoolsDeps
from conan.tools.layout import basic_layout
from conan.tools.files import get, chmod
from os.path import join


class openocd(ConanFile):
    name = "openocd"
    package_type = "application"
    win_bash = True
    version = "latest"
    license = "GPL-2.0-or-later"
    author = "<Shin Umeda> <umeda.shin@gmail.com>"
    url = "https://sourceforge.net/p/openocd/code/ci/master/tree/"
    description = "The Open On-Chip Debugger"
    topics = "debug"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.tool_requires("autoconf/2.71")
        self.tool_requires("automake/1.16.5")
        self.tool_requires("libtool/2.4.7")
        self.tool_requires("pkgconf/2.2.0")
        self.requires("jimtcl/0.83")
        self.requires("zlib/1.3.1")
        self.requires("openssl/3.5.2")
        self.requires("libusb/1.0.26")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        chmod(self, join(self.source_folder, "src", "helper", "bin2char.sh"), execute=True)

    def layout(self):
        basic_layout(self)

    def generate(self):
        deps = AutotoolsDeps(self)
        deps.generate()
        at_toolchain = AutotoolsToolchain(self)
        at_toolchain.configure_args.append("--disable-werror")
        at_toolchain.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.autoreconf()
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()
