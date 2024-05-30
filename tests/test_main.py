'''
Test module.
'''

from netcdfqc.main import get_version

def test_get_version() -> str:
    '''
    Temporary test for the temporary get_version function.
    '''
    assert get_version() == "0.1.0"
