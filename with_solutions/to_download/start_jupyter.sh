#!/bin/bash
#
# start_jupyter.sh
# Copyright (C) 2021 Uwe Schmitt <uwe.schmitt@id.ethz.ch>
#
# Distributed under terms of the MIT license.
#

# https://stackoverflow.com/questions/4774054
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd ${SCRIPTPATH}

source ./vars.sh

if command -v conda >/dev/null; then
    PYTHON_EXE=$(conda run -n base python -c 'import sys; print(sys.executable)')
    BIN_FOLDER=$(dirname ${PYTHON_EXE})
else
    BIN_FOLDER=~/miniconda3/bin
fi

echo "found conda binaries at ${BIN_FOLDER}"
source ${BIN_FOLDER}/activate ${ENVNAME}


cd $(dirname ${SCRIPTPATH})

jupyter lab --allow-root .
