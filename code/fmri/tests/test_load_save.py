import pytest 
from fmri.load_save import find_derivative

@pytest.mark.parametrize(
    ('path', 'expected_der_path'),
    [
        ('/home/hcph/fmriprep', '/home/hcph/fmriprep/derivatives'),
        ('/home/hcph-derivatives', '/home/hcph-derivatives'),
        ('/home/derivatives', '/home/derivatives'),
        ('/home/derivatives/fmriprep', '/home/derivatives')
    ],
)
def test_find_derivative(path, expected_der_path):
    der_path = find_derivative(path)
    assert der_path == expected_der_path
