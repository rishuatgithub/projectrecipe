#!/bash/bin

CONDA_PROJECTRECIPE_ENV=projectrecipeenv
CONDA_PYTHON_VERSION=3.8

sudo yum update -y
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
source "$HOME/miniconda/etc/profile.d/conda.sh"
hash -r
conda config --set always_yes yes --set changeps1 no
conda config --add channels conda-forge
conda update -n base -c defaults conda
conda create --name $CONDA_PROJECTRECIPE_ENV python=$CONDA_PYTHON_VERSION
conda activate $CONDA_PROJECTRECIPE_ENV
conda install --file requirements.txt