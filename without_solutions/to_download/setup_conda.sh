#!/bin/bash
#
# setup_conda.sh
# Copyright (C) 2022 Uwe Schmitt <uwe.schmitt@id.ethz.ch>
#
# Distributed under terms of the MIT license.
#

set -e
shopt -s extdebug

# https://stackoverflow.com/questions/4774054
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd "${SCRIPTPATH}"

source ./vars.sh

# https://stackoverflow.com/questions/64786/error-handling-in-bash
error() {
    local parent_lineno="$1"
    local message="$2"
    local code="${3:-1}"

    echo
    echo
    if [[ -n $message ]]; then
        echo "Error on or near line ${parent_lineno}: ${message}; exiting with status ${code}"
    else
        echo "Error on or near line ${parent_lineno}; exiting with status ${code}"
    fi
    exit "${code}"
}
trap 'error ${LINENO}' ERR

BREW=

if [[ ${OSTYPE} = darwin* ]]; then
    if [[ $(uname -m) == "x86_64" ]]; then
        test -f /usr/local/bin/brew || {
            echo "please install homebrew https://brew.sh/ first"
            exit 1;
        }
        BREW=/usr/local/bin/brew
    else
        test -f /opt/homebrew/bin/brew || {
            echo "please install homebrew from https://brew.sh/ for M1 first"
            exit 1;
        }
        BREW=/opt/homebrew/bin/brew
   fi
fi


function install_minicoda_if_needed {
    URL="$1"
    shift # else the source ... activate below blows up

    if command -v conda >/dev/null; then
        PYTHON_EXE=$(conda run -n base python -c 'import sys; print(sys.executable)')
        echo "found conda binaries at $(dirname ${PYTHON_EXE})"
        source $(dirname ${PYTHON_EXE})/activate
        return
    fi

    if ! test -d ~/miniconda3; then
        echo
        echo "download and install miniconda"
        echo
        wget "${URL}" -O /tmp/miniconda.sh
        bash /tmp/miniconda.sh -b -p ~/miniconda3
        rm /tmp/miniconda.sh
    fi
    source ~/miniconda3/bin/activate
}


function write_pythran_rc {

    [[ ${OSTYPE} != darwin* ]] && return

    SETTINGS="[compiler]\nblas=openblas\ninclude_dirs=$($BREW --prefix)/opt/openblas/include\nlibrary_dirs=$($BREW --prefix)/opt/openblas/lib\n"

    if test -f ~/.pythranrc; then
        echo
        echo "the file ~/.pythranrc already exists."
        echo "please copy paste the following lines and edit the file to include"
        echo "the following settings:"
        echo "----"
        printf ${SETTINGS}
        echo "----"
        echo
        read -p "please press any key to continue" -n 1 -r
        return
    fi
    printf ${SETTINGS} > ~/.pythranrc
}


function prepare_machine {

    case "${OSTYPE}" in
    darwin*)
        if [[ $(uname -m) == "x86_64" ]]; then
            PYPYURL=https://downloads.python.org/pypy/pypy3.9-v7.3.9-osx64.tar.bz2
        else
            PYPYURL=https://buildbot.pypy.org/nightly/py3.9/pypy-c-jit-latest-macos_arm64.tar.bz2
        fi
        ;;
    linux*)
        PYPYURL=https://downloads.python.org/pypy/pypy3.9-v7.3.9-linux64.tar.bz2
        ;;
    *)
        echo "unknown: OSTYPE=${OSTYPE}"
        exit 1
        ;;
    esac

    PYPYTAR=/tmp/$(basename $PYPYURL)
    test -f "${PYPYTAR}" || wget -O "${PYPYTAR}" $PYPYURL

    case "${OSTYPE}" in
    darwin*)
        $BREW install wget graphviz openblas
        install_minicoda_if_needed https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-$(uname -m).sh
        ;;
    linux*)
	SUDO=sudo
	[[ $(id -u) = 0 ]] && SUDO=
        $SUDO apt update && $SUDO apt upgrade -y
        $SUDO apt install -y build-essential git vim wget curl graphviz libcurl4-gnutls-dev libgnutls28-dev
        install_minicoda_if_needed https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
        ;;
    esac
}

function setup_conda_environment {

    if conda env list | grep miniconda3 | grep --silent "/${ENVNAME}$"; then
        echo
        echo "The conda environment ${ENVNAME} already exists. This might be because"
        echo "your previous attempt failed and left a broken / incomplete environment."
        read -p "Do you want to delete and recreate the environment [y/n]? " -n 1 -r
        echo
        if [[ ! "${REPLY}" =~ ^[Yy]$ ]]; then
            echo
            echo setup cancelled
            exit 1
        fi
        echo
        echo "delete existing environment"
        conda env remove --yes -n "${ENVNAME}"
        echo
    fi

    conda create -n "${ENVNAME}" -y python=3.10
    CONDA_PYTHON=$(conda run -n base python -c 'import sys; print(sys.executable)')
    CONDA_ROOT=$(dirname $(dirname $CONDA_PYTHON))
    python=${CONDA_ROOT}/envs/${ENVNAME}/bin/python
    echo "python at" $($python -c 'import sys; print(sys.executable)')

    $python -m pip install -U pip wheel setuptools
    $python -m pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org
    $python -m pip install --no-cache-dir brotlipy
    $python -m pip install --no-cache-dir -r requirements.txt
}

function setup_pypy {
    echo "conda prefix" ${CONDA_PREFIX}
    mkdir -p "${CONDA_PREFIX}/pypy"
    tar xf ${PYPYTAR} -C "${CONDA_PREFIX}/pypy" --strip-component=1
    rm -f "${CONDA_PREFIX}/bin/pypy{,3}"
    for U in pypy pypy3; do
        for P in ${CONDA_PREFIX}/bin ${CONDA_PREFIX}/envs/${ENVNAME}/bin; do
            test -f $P/$U && rm $P/$U
            ln -s ${CONDA_PREFIX}/pypy/bin/$U $P/$U
        done
    done

    pypy -m ensurepip
    pypy -m pip install --no-cache-dir -U pip wheel setuptools

    if [[ ${OSTYPE} == darwin* ]]; then
        OPENBLAS=$($BREW --prefix openblas 2>/dev/null)
        NPY_BLAS_ORDER='openblas'
    fi

    OPENBLAS="${OPENBLAS}"  NPY_BLAS_ORDER="${NPY_BLAS_ORDER}" pypy -m pip install --no-cache-dir -r pypy_requirements.txt
}


function fix_jupyterlab_black_issue {
    # somehow the black plugin in jupyterlab assumes on some computers that the
    # following folder already exists:
    mkdir -p ~/.cache/black/22.6/
}

prepare_machine
setup_conda_environment
setup_pypy
fix_jupyterlab_black_issue
write_pythran_rc

echo
echo setup done.
