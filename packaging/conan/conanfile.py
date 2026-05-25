from conan import ConanFile
from conan.tools.files import copy
import os


class NwauCAbiConan(ConanFile):
    name = "nwau-c-abi"
    version = "0.1.0"
    license = "Apache-2.0"
    author = "edithatogo"
    url = "https://github.com/edithatogo/mchs"
    homepage = "https://github.com/edithatogo/mchs"
    description = "C ABI scaffold for MCHS/NWAU interoperability."
    topics = ("health-economics", "nwau", "c-abi", "rust")
    settings = "os", "arch", "compiler", "build_type"
    package_type = "library"

    def export_sources(self):
        repo_root = os.path.abspath(os.path.join(self.recipe_folder, "..", ".."))
        copy(
            self,
            "*",
            src=os.path.join(repo_root, "rust"),
            dst=os.path.join(self.export_sources_folder, "rust"),
        )
        copy(self, "LICENSE", src=repo_root, dst=self.export_sources_folder)

    def build(self):
        self.run(
            "cargo build --release --locked -p nwau-c-abi",
            cwd=os.path.join(self.source_folder, "rust"),
        )

    def package(self):
        copy(
            self,
            "nwau_abi.h",
            src=os.path.join(
                self.source_folder, "rust", "crates", "nwau-c-abi", "include"
            ),
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            "libnwau_c_abi.a",
            src=os.path.join(self.source_folder, "rust", "target", "release"),
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "libnwau_c_abi.so*",
            src=os.path.join(self.source_folder, "rust", "target", "release"),
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "libnwau_c_abi*.dylib",
            src=os.path.join(self.source_folder, "rust", "target", "release"),
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "nwau_c_abi.lib",
            src=os.path.join(self.source_folder, "rust", "target", "release"),
            dst=os.path.join(self.package_folder, "lib"),
            keep_path=False,
        )
        copy(
            self,
            "nwau_c_abi.dll",
            src=os.path.join(self.source_folder, "rust", "target", "release"),
            dst=os.path.join(self.package_folder, "bin"),
            keep_path=False,
        )
        copy(
            self,
            "LICENSE",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )

    def package_info(self):
        self.cpp_info.libs = ["nwau_c_abi"]
