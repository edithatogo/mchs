import hashlib
import os
import tarfile

from conan import ConanFile
from conan.tools.files import copy, download


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
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    package_type = "library"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def source(self):
        source_data = self.conan_data["sources"][self.version]
        archive_path = os.path.join(self.source_folder, "source.tar.gz")
        download(self, source_data["url"], archive_path)
        with open(archive_path, "rb") as archive_file:
            digest = hashlib.sha512(archive_file.read()).hexdigest()
        if digest != source_data["sha512"]:
            raise ValueError(
                f"Archive SHA512 mismatch for {source_data['url']}: {digest}"
            )
        destination = os.path.abspath(self.source_folder)
        with tarfile.open(archive_path, "r:gz") as archive:
            for member in archive.getmembers():
                path_parts = member.name.split("/", 1)
                if len(path_parts) != 2 or not path_parts[1]:
                    continue
                member.name = path_parts[1]
                target = os.path.abspath(os.path.join(destination, member.name))
                if not target.startswith(destination + os.sep):
                    raise ValueError(f"Unsafe archive path: {member.name}")
                archive.extract(member, destination)

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
        self.cpp_info.set_property("cmake_file_name", "nwau-c-abi")
        self.cpp_info.set_property("cmake_target_name", "nwau-c-abi::nwau-c-abi")
