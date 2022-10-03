#!/bin/bash
#
# check_setup.sh
# Copyright (C) 2022 Uwe Schmitt <uwe.schmitt@id.ethz.ch>
#
# Distributed under terms of the MIT license.
#


set -e
# https://stackoverflow.com/questions/4774054
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

function setup {

    ERRORFILE=/tmp/errors.txt
    ERROR=0
    cd ${SCRIPTPATH}

    source ./vars.sh

    if command -v conda >/dev/null; then
        PYTHON_EXE=$(conda run -n base python -c 'import sys; print(sys.executable)')
        BIN_FOLDER=$(dirname ${PYTHON_EXE})
    else
        BIN_FOLDER=~/miniconda3/bin
    fi

    echo "Found conda binaries at ${BIN_FOLDER}"
    if source ${BIN_FOLDER}/activate ${ENVNAME}; then
        echo Conda environment activated
    else
        echo Conda environment activation failed.
        exit 1
    fi

    cd $(dirname ${SCRIPTPATH})

    rm -f ${ERRORFILE}
}

function check_cython {

    echo -n 'Check cython: '

    cat > /tmp/print_42.pyx <<__EOF
#cython: language_level=3
print(42)
__EOF

    if PYTHONPATH="/tmp" python -c 'import pyximport; pyximport.install(); import print_42' >> ${ERRORFILE} 2>&1; then
        echo "passed"
    else
        echo "failed"
        ERROR=1
    fi
}

function check_pythran {
    echo -n 'Check pythran: '
    cat > /tmp/test_pythran.py<<__EOF
import numpy as np
#pythran export test(int)
def test(n):
    return np.sum(np.arange(n))
__EOF
    pushd /tmp >/dev/null
    if pythran test_pythran.py >> ${ERRORFILE} 2>&1; then
        echo "passed";
    else
        echo "please check https://pythran.readthedocs.io/en/latest/#installation if you need to install extra libraries";
        ERROR=1
    fi
    popd >/dev/null
}


function check_pypy {
    echo -n 'Check pypy: '
    if pypy -c 'import numpy' >> ${ERRORFILE} 2>&1; then
        echo "passed"
    else
        echo "failed"
        ERROR=1
    fi
}


function check_graphviz {
    echo -n 'Check graphviz: '
    if dot -V >> ${ERRORFILE} 2>&1; then
        echo "passed"
    else
        echo "failed"
        ERROR=1
    fi
}

function check_library {
    echo -n "Check $1: "
    if python -c "${2:-import $1}" >> ${ERRORFILE} 2>&1; then
        echo "passed"
    else
        echo "failed"
        ERROR=1
    fi

}

function finalize {
    if (( ${ERROR} == 0 )); then
        echo "Congratulations: all tests succeeded :-)"
    else
        echo "Oops. At least one test failed :-("
        echo "You can check ${ERRORFILE} for details"
    fi
}

setup
check_library numpy
check_library scipy
check_library matplotlib 'import matplotlib.pyplot as plt; plt.figure()'
check_graphviz
check_cython
check_pythran
check_pypy
finalize
