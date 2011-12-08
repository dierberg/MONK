require hydraip-image.bb

DEPENDS = "hydraip-image hidav-bootable-sdcard"

PR = "r3"

export IMAGE_BASENAME = "hydraip-devimage"

IMAGE_FSTYPES = "tar.bz2"

# SDK
IMAGE_INSTALL += " \
  task-native-sdk \
  gdb \
  gdbserver \
  openssh-sftp-server \
  subversion \
  git \ 
"
