from conans import ConanFile, CMake
from conans import tools
import os
import textwrap

class CExceptionConan(ConanFile):
    name = "cexception"
    license = "MIT"
    url = "https://github.com/ThrowTheSwitch/CException"
    description = "Conan wrap around cexception"
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
        self._cmake.definitions["CEXCEPTION_VERSION_STRING"] = self.version
        self._cmake.definitions["CEXCEPTION_VERSION_MAJOR"] = tools.Version(self.version).major
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

    @staticmethod
    def _create_cmake_module_variables(module_file):
        content = textwrap.dedent("""\
            if(DEFINED CEXCEPTION_FOUND)
                set(CEXCEPTION_FOUND ${CEXCEPTION_FOUND})
                set(CEXCEPTION_NEED_PREFIX TRUE)
            endif()
            if(DEFINED CEXCEPTION_INCLUDE_DIR)
                set(CEXCEPTION_INCLUDE_DIRS ${CEXCEPTION_INCLUDE_DIR})
                set(CEXCEPTION_INCLUDE_DIR ${CEXCEPTION_INCLUDE_DIR})
            endif()
            if(DEFINED CEXCEPTION_LIBRARIES)
                set(CEXCEPTION_LIBRARIES ${CEXCEPTION_LIBRARIES})
            endif()
            if(DEFINED CEXCEPTION_VERSION)
                set(CEXCEPTION_VERSION_STRING ${CEXCEPTION_VERSION})
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
        self.cpp_info.names["cmake_find_package"] = "CEXCEPTION"
        self.cpp_info.names["cmake_find_package_multi"] = "CEXCEPTION"
        self.cpp_info.builddirs.append(self._module_subfolder)
        self.cpp_info.build_modules["cmake_find_package"] = [os.path.join(self._module_subfolder, self._module_file)]
        self.cpp_info.libs = ["cexception"]
