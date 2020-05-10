from reading_content_parallel import * 
import os 


def test_getFilename(): 
    assert getFilename('l1')  == 'data/jamieoliverdata_l1.json'


def test_checkiffileexists(): 
    test_filename = 'reading_config.py'
    assert checkiffileexists('reading_config.py') == os.path.isfile(test_filename)
