# Debug

This packages a recent version of OpenOCD and jimtcl for usage from
conan. The reason why it's a random recent commit is because OpenOCD
has no releases that support rp2350, despite it being supported in the
main branch. jimtcl is also packaged because it is required by OpenOCD.

# Usage

Add `self.tool_requires("openocd/latest")` to the conanfile, or add it via
a profile. Then source conanbuild.sh to get access to openocd.

