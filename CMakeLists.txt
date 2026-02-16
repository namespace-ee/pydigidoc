cmake_minimum_required(VERSION 3.20)
project(pydigidoc VERSION 0.0.1 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Upstream uses CMAKE_SOURCE_DIR for paths to etc/ and cmake/modules/.
# When included via add_subdirectory(), CMAKE_SOURCE_DIR is our root,
# not the submodule root. Create symlinks (or copies on Windows) so
# those references resolve.
foreach(_DIR etc cmake)
    if(NOT EXISTS ${CMAKE_SOURCE_DIR}/${_DIR})
        if(WIN32)
            file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/libdigidocpp/${_DIR}
                DESTINATION ${CMAKE_SOURCE_DIR})
        else()
            file(CREATE_LINK
                libdigidocpp/${_DIR}
                ${CMAKE_SOURCE_DIR}/${_DIR}
                SYMBOLIC)
        endif()
    endif()
endforeach()

# Suppress upstream's SWIG/tools/framework/docs builds
set(CMAKE_DISABLE_FIND_PACKAGE_SWIG TRUE)
set(CMAKE_DISABLE_FIND_PACKAGE_Doxygen TRUE)
set(CMAKE_DISABLE_FIND_PACKAGE_Boost TRUE)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(BUILD_TOOLS OFF CACHE BOOL "" FORCE)
set(FRAMEWORK OFF CACHE BOOL "" FORCE)

# Skip upstream install(EXPORT) — fails with static builds because minizip
# and digidocpp_priv aren't in the export set. We don't need the export config.
set(ANDROID TRUE)

# On macOS, prefer Homebrew's libxml2 over Xcode SDK to avoid ABI mismatches.
# Homebrew xmlsec1 links Homebrew libxml2 2.15+, but CMake finds SDK libxml2 2.9;
# the ABI difference causes segfaults at runtime. Homebrew libxml2 is keg-only,
# so we must point CMake to its specific prefix.
if(APPLE AND NOT DEFINED LibXml2_ROOT)
    execute_process(
        COMMAND brew --prefix libxml2
        OUTPUT_VARIABLE _HOMEBREW_LIBXML2
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
        RESULT_VARIABLE _BREW_RESULT)
    if(_BREW_RESULT EQUAL 0 AND _HOMEBREW_LIBXML2)
        set(LibXml2_ROOT ${_HOMEBREW_LIBXML2})
    endif()
endif()

# Disable upstream install() rules entirely — they fail on Windows with static
# builds due to $<TARGET_PDB_FILE:...> on targets that are static or don't exist.
# We define our own install rules below.
set(CMAKE_SKIP_INSTALL_RULES ON)
add_subdirectory(libdigidocpp EXCLUDE_FROM_ALL)
set(CMAKE_SKIP_INSTALL_RULES OFF)

unset(ANDROID)
set(CMAKE_DISABLE_FIND_PACKAGE_SWIG FALSE)

# Verify upstream SWIG interface has the expected module declaration
file(STRINGS ${CMAKE_CURRENT_SOURCE_DIR}/libdigidocpp/libdigidocpp.i _SWIG_MODULE_LINE
    REGEX "%module.*digidoc")
if(NOT _SWIG_MODULE_LINE)
    message(FATAL_ERROR "Upstream libdigidocpp.i missing expected %module digidoc declaration")
endif()

# Our SWIG bindings
find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
find_package(SWIG 4.0 REQUIRED COMPONENTS python)
include(UseSWIG)

cmake_policy(SET CMP0078 NEW)
cmake_policy(SET CMP0086 NEW)
set(UseSWIG_TARGET_NAME_PREFERENCE STANDARD)

set(SWIG_SOURCE ${CMAKE_CURRENT_SOURCE_DIR}/swig/pydigidoc.i)
set_property(SOURCE ${SWIG_SOURCE} PROPERTY CPLUSPLUS ON)
set_property(SOURCE ${SWIG_SOURCE} PROPERTY SWIG_MODULE_NAME digidoc)
set_property(SOURCE ${SWIG_SOURCE} PROPERTY USE_SWIG_DEPENDENCIES TRUE)
set_property(SOURCE ${SWIG_SOURCE} PROPERTY INCLUDE_DIRECTORIES
    ${CMAKE_CURRENT_SOURCE_DIR}/libdigidocpp
    ${CMAKE_CURRENT_SOURCE_DIR}/libdigidocpp/src)

swig_add_library(pydigidoc_swig
    TYPE MODULE LANGUAGE python
    OUTPUT_DIR ${CMAKE_BINARY_DIR}/pydigidoc
    OUTFILE_DIR ${CMAKE_BINARY_DIR}/swig_generated
    SOURCES ${SWIG_SOURCE})

target_include_directories(pydigidoc_swig PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/libdigidocpp/src
    ${Python3_INCLUDE_DIRS})

set_target_properties(pydigidoc_swig PROPERTIES
    OUTPUT_NAME "_digidoc"
    PREFIX ""
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/pydigidoc)

target_link_libraries(pydigidoc_swig PRIVATE
    digidocpp digidocpp_util Python3::Module)

if(APPLE)
    set_target_properties(pydigidoc_swig PROPERTIES
        INSTALL_RPATH "@loader_path"
        BUILD_WITH_INSTALL_RPATH TRUE)
endif()

# Install into wheel (scikit-build-core wheel.install-dir = "pydigidoc")
install(TARGETS pydigidoc_swig LIBRARY DESTINATION . RUNTIME DESTINATION .)
install(FILES ${CMAKE_BINARY_DIR}/pydigidoc/digidoc.py DESTINATION .)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/pydigidoc/__init__.py DESTINATION .)

# Install runtime data (schema files, config) so the library works from the wheel
set(_SCHEMA_DIR ${CMAKE_CURRENT_SOURCE_DIR}/libdigidocpp/etc/schema)
install(FILES
    ${CMAKE_BINARY_DIR}/libdigidocpp/src/digidocpp.conf
    ${_SCHEMA_DIR}/conf.xsd
    ${_SCHEMA_DIR}/OpenDocument_manifest_v1_2.xsd
    ${_SCHEMA_DIR}/xmldsig-core-schema.xsd
    ${_SCHEMA_DIR}/XAdES01903v132-201601.xsd
    ${_SCHEMA_DIR}/XAdES01903v141-201601.xsd
    ${_SCHEMA_DIR}/en_31916201v010101.xsd
    ${_SCHEMA_DIR}/OpenDocument_dsig.xsd
    DESTINATION schema)
