#!/bin/sh

ROOT_DIRS="/home/iridium/data/archive /home/iridium/data/raw /home/socket/data/archive /home/socket/data/raw"

for ROOT_DIR in $ROOT_DIRS
do
  DIRS_TO_TAR=`find ${ROOT_DIR}/ -type d -mtime +30`
  if [ ! -z "${DIRS_TO_TAR}" ]; then
    for DIR_TO_TAR in $DIRS_TO_TAR
    do
      DIR_NAME=`echo "${DIR_TO_TAR}" | xargs -n 1 basename`
      if echo "${DIR_NAME}" | grep -qE '^[0-9]{8}$'; then
        tar -cvzf ${ROOT_DIR}/${DIR_NAME}.tar.gz ${ROOT_DIR}/${DIR_NAME}
        if [ $? -eq 0 ]; then
          rm -rf ${ROOT_DIR}/${DIR_NAME}
        fi
      fi
    done
  fi
done
