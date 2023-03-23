from zkpy.ptau import PTau
from distutils import dir_util
from pytest import fixture
from pytest import raises
import os
from pathlib import Path
import subprocess


# Uses existing test files for better unit test isolation
@fixture
def datadir(tmpdir, request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))
    return Path(tmpdir)


def test_ptau_start_creates_new_file(tmp_path, datadir):
    ptau = PTau(working_dir=tmp_path)
    ptau.start()
    ptau_file = tmp_path / ptau.ptau_file
    assert ptau_file.exists()


def test_ptau_contribute_creates_new_file(tmp_path, datadir):
    ptau_file_start = datadir / "start.ptau"
    ptau = PTau(ptau_file=ptau_file_start, working_dir=tmp_path)
    ptau.contribute()
    ptau_file_contrib = tmp_path / ptau.ptau_file
    assert ptau_file_start != ptau_file_contrib
    assert ptau_file_contrib.exists()


def test_ptau_beacon_creates_new_file(tmp_path, datadir):
    ptau_file_contribute = datadir / "contributed.ptau"
    ptau = PTau(ptau_file=ptau_file_contribute, working_dir=tmp_path)
    ptau.beacon()
    ptau_file_beacon = tmp_path / ptau.ptau_file
    assert ptau_file_beacon != ptau_file_contribute
    assert ptau_file_beacon.exists()


def test_ptau_phase2_creates_new_file(tmp_path, datadir):
    ptau_file_beaconed = datadir / "beaconed.ptau"
    ptau = PTau(ptau_file=ptau_file_beaconed, working_dir=tmp_path)
    ptau.prep_phase2()
    ptau_file_phase2 = tmp_path / ptau.ptau_file
    assert ptau_file_phase2 != ptau_file_beaconed
    assert ptau_file_phase2.exists()


def test_verify_fails_if_file_changed(tmp_path, datadir):
    with raises(subprocess.CalledProcessError):
        ptau_file_contribute = datadir / "contributed.ptau"
        ptau = PTau(ptau_file=ptau_file_contribute, working_dir=tmp_path)
        with ptau_file_contribute.open("w") as f:
            f.write('asdjfakjsfk')
        assert ptau.verify() is False
