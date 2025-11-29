{
  "variables": {
    'openssl_fips': ''
  },
  "targets": [{
    "target_name": "classic_level",
    "conditions": [
      ["OS == 'linux'", {
        "cflags": [],
        "cflags!": [ "-fno-tree-vrp"]
      }],
      ["OS == 'mac'", {
        "cflags+": ["-fvisibility=hidden"],
        "xcode_settings": {
          # -fvisibility=hidden
          "GCC_SYMBOLS_PRIVATE_EXTERN": "YES",

          # Set minimum target version because we're building on newer
          # Same as https://github.com/nodejs/node/blob/v10.0.0/common.gypi#L416
          "MACOSX_DEPLOYMENT_TARGET": "10.7",

          # Build universal binary to support M1 (Apple silicon)
          "OTHER_CFLAGS": [
            "-arch x86_64",
            "-arch arm64"
          ],
          "OTHER_LDFLAGS": [
            "-arch x86_64",
            "-arch arm64"
          ]
        }
      }],
      ["OS == 'android'", {
        "cflags": [ "-fPIC" ],
        "ldflags": [ "-fPIC", "-Wl", "-z", "max-page-size=16384" ],
        "cflags!": [
          "-fno-tree-vrp",
          "-mfloat-abi=hard",
          "-fPIE"
        ],
        "ldflags!": [ "-fPIE" "-Wl", "-z", "max-page-size=16384" ]
      }],
      ["target_arch == 'arm'", {
        "cflags": [ "-mfloat-abi=hard" ]
      }]
    ],
    "dependencies": [
      "<(module_root_dir)/deps/leveldb/leveldb.gyp:leveldb"
    ],
    "include_dirs"  : [
      "<!(node -e \"require('napi-macros')\")"
    ],
    "sources": [
      "binding.cc"
    ]
  }]
}
