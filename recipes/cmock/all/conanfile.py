from conans import ConanFile, CMake
from conans import tools
import os
import textwrap

class CMockConan(ConanFile):
    requires = "unity/2.5.2"
    name = "cmock"
    license = "MIT"
    url = "https://github.com/ThrowTheSwitch/CMock"
    description = "Conan wrap around cmock"
    topics = ("todo")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = ["make", "cmake"]
    exports_sources = ["*"]
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["CMOCK_VERSION_STRING"] = self.version
        self._cmake.definitions["CMOCK_VERSION_MAJOR"] = tools.Version(self.version).major
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self._create_cmake_module_variables(
            os.path.join(self.package_folder, self._module_subfolder, self._module_file)
        )
        self.copy("*.rb", dst="scripts", src=(self._source_subfolder + "/scripts"))
        self.copy("*.rb", dst="lib", src=(self._source_subfolder + "/lib"))
        self.copy("*.rb", dst="config", src=(self._source_subfolder + "/config"))

    @staticmethod
    def _create_cmake_module_variables(module_file):
        content = textwrap.dedent("""\
            if(DEFINED CMOCK_FOUND)
                set(CMOCK_FOUND ${CMOCK_FOUND})
                set(CMOCK_NEED_PREFIX TRUE)
            endif()
            if(DEFINED CMOCK_INCLUDE_DIR)
                set(CMOCK_INCLUDE_DIRS ${CMOCK_INCLUDE_DIR})
                set(CMOCK_INCLUDE_DIR ${CMOCK_INCLUDE_DIR})
            endif()
            if(DEFINED CMOCK_LIBRARIES)
                set(CMOCK_LIBRARIES ${CMOCK_LIBRARIES})
            endif()
            if(DEFINED CMOCK_VERSION)
                set(CMOCK_VERSION_STRING ${CMOCK_VERSION})
            endif()
        """)
        tools.save(module_file, content)

    @property
    def _module_subfolder(self):
        return os.path.join("lib", "cmake")

    @property
    def _module_file(self):
        return "conan-official-{}-variables.cmake".format(self.name)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "CMOCK"
        self.cpp_info.names["cmake_find_package_multi"] = "CMOCK"
        self.cpp_info.builddirs.append(self._module_subfolder)
        self.cpp_info.build_modules["cmake_find_package"] = [os.path.join(self._module_subfolder, self._module_file)]
        self.cpp_info.libs = ["cmock"]
        self.cpp_info.bindirs = ['lib']
