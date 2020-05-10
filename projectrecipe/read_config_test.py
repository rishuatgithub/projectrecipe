import pytest
from read_config import getconfig

### testing read_config.py


def test_read_config(): 
    assert getconfig()['PRCONFIG']['AWS']['PROFILE'] == 'dev'
    assert getconfig()['PRCONFIG']['GENERAL']['HOME_DIR'] == 'projectrecipe'