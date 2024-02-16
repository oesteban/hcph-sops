import pytest
import os.path as op
import fmri.load_save as fl


@pytest.mark.parametrize(
    ("path", "expected_der_path"),
    [
        ("/home/hcph/fmriprep", "/home/hcph/fmriprep/derivatives"),
        ("/home/hcph-derivatives", "/home/hcph-derivatives"),
        ("/home/derivatives", "/home/derivatives"),
        ("/home/derivatives/fmriprep", "/home/derivatives"),
        ("/home/derivatives/fmriprep/23.2.0", "/home/derivatives"),
    ],
)
def test_find_derivative(path, expected_der_path):
    der_path = fl.find_derivative(path)
    assert der_path == expected_der_path


@pytest.mark.parametrize(
    ("path", "expected_dim"),
    [
        ("/home/DiFuMo2-LP", 2),
        ("/home/DiFuMo64", 64),
        ("/home/DiFuMo128", 128),
        ("/home/DiFuMo-LP", None),
        ("/home/Yeo", None),
    ],
)
def test_find_atlas_dimension(path, expected_dim):
    if expected_dim is not None:
        atlas_dim = fl.find_atlas_dimension(path)
        assert atlas_dim == expected_dim
    else:
        with pytest.raises(ValueError):
            fl.find_atlas_dimension(path)


"""
@pytest.mark.parametrize('return_existing', [False, True])
def test_check_existing_output(return_existing, monkeypatch):
    output = ""
    func_filename = ["sub-1.txt", "sub-2.txt"]
    existing_filenames = ["sub-2.txt"]

    FAKE_PATTERN: list = [
    "sub-{subject}"
    "_{extension}"
    ]

    def mock_exists(file_path):
        return file_path in existing_filenames
    
    monkeypatch.setattr(op, 'exists', mock_exists)

    if return_existing:
        missing_file, existing_file = fl.check_existing_output(output,func_filename, return_existing=return_existing, patterns=FAKE_PATTERN)
        assert missing_file == ['sub-1.txt']
        assert existing_file == ['sub-2.txt']
    else:
        missing_file = fl.check_existing_output(output,func_filename, return_existing=return_existing, patterns=FAKE_PATTERN)
        assert missing_file == ['sub-2.txt']
"""
