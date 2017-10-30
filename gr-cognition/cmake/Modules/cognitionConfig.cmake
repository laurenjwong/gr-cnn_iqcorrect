INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_COGNITION cognition)

FIND_PATH(
    COGNITION_INCLUDE_DIRS
    NAMES cognition/api.h
    HINTS $ENV{COGNITION_DIR}/include
        ${PC_COGNITION_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    COGNITION_LIBRARIES
    NAMES gnuradio-cognition
    HINTS $ENV{COGNITION_DIR}/lib
        ${PC_COGNITION_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(COGNITION DEFAULT_MSG COGNITION_LIBRARIES COGNITION_INCLUDE_DIRS)
MARK_AS_ADVANCED(COGNITION_LIBRARIES COGNITION_INCLUDE_DIRS)

