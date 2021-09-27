cmake_minimum_required(VERSION 3.4)
project(cmock C)

include(GNUInstallDirs)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(unity)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(MSVC OR MSVC90 OR MSVC10)
    set(MSVC ON)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

set(SOURCE_SUBFOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/src)
set(CMOCK_LIBRARY cmock)
set(CMOCK_TARGETS ${CMOCK_LIBRARY})

add_library(${CMOCK_LIBRARY}  ${SOURCE_SUBFOLDER}/cmock.c)
target_include_directories(${CMOCK_LIBRARY} PRIVATE ${SOURCE_SUBFOLDER})

set_target_properties(${CMOCK_LIBRARY} PROPERTIES VERSION ${CMOCK_VERSION_STRING} SOVERSION ${CMOCK_VERSION_MAJOR})

install(TARGETS ${CMOCK_TARGETS}
        BUNDLE DESTINATION ${CMAKE_INSTALL_BINDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(FILES
    ${SOURCE_SUBFOLDER}/cmock.h
    ${SOURCE_SUBFOLDER}/cmock_internals.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

