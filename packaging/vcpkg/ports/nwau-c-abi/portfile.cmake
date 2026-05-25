# Draft vcpkg portfile for the in-repository NWAU C ABI surface.
#
# This file is intentionally kept in the MCHS repository as local readiness
# evidence. Upstream vcpkg submission still requires moving the port into the
# vcpkg registry, adding registry version metadata, and validating against
# vcpkg's CI policy.

vcpkg_from_github(
    OUT_SOURCE_PATH SOURCE_PATH
    REPO edithatogo/mchs
    REF 2f658d43be016116ae31b8bdccef9c0ab986fca5
    SHA512 e3c533ac2bfdae49afd7da8a16cfe66d4a3dcf3d9f242015ff29540000e81f79c33df5ad1f92076538659b53429f2ba00e746f10d141d6cdcc0a8a291899eacd
    HEAD_REF master
)

vcpkg_execute_required_process(
    COMMAND cargo build --release --locked -p nwau-c-abi
    WORKING_DIRECTORY "${SOURCE_PATH}/rust"
    LOGNAME build-${TARGET_TRIPLET}
)

file(INSTALL
    "${SOURCE_PATH}/rust/crates/nwau-c-abi/include/nwau_abi.h"
    DESTINATION "${CURRENT_PACKAGES_DIR}/include"
)

if(VCPKG_TARGET_IS_WINDOWS)
    file(GLOB NWAU_LIBS
        "${SOURCE_PATH}/rust/target/release/*.lib"
    )
    file(GLOB NWAU_DLLS
        "${SOURCE_PATH}/rust/target/release/*.dll"
    )
    file(INSTALL ${NWAU_LIBS} DESTINATION "${CURRENT_PACKAGES_DIR}/lib")
    file(INSTALL ${NWAU_DLLS} DESTINATION "${CURRENT_PACKAGES_DIR}/bin")
else()
    file(GLOB NWAU_LIBS
        "${SOURCE_PATH}/rust/target/release/libnwau_c_abi.a"
        "${SOURCE_PATH}/rust/target/release/libnwau_c_abi.*.dylib"
        "${SOURCE_PATH}/rust/target/release/libnwau_c_abi.so"
    )
    file(INSTALL ${NWAU_LIBS} DESTINATION "${CURRENT_PACKAGES_DIR}/lib")
endif()
vcpkg_install_copyright(FILE_LIST "${SOURCE_PATH}/LICENSE")
