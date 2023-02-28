from zkpy.ptau import PTau

def test_ptau_start_creates_new_file(tmp_path):
    ptau = PTau(working_dir=tmp_path)
    ptau.start()
    ptau_file = tmp_path / ptau.ptau_file
    assert ptau_file.exists()

def test_ptau_contribute_creates_new_file(tmp_path):
    ptau = PTau(working_dir=tmp_path)
    ptau.start()
    ptau_file_start = tmp_path / ptau.ptau_file
    assert ptau_file_start.exists()
    ptau.contribute()
    ptau_file_contrib = tmp_path / ptau.ptau_file
    assert ptau_file_start != ptau_file_contrib 
    assert ptau_file_contrib.exists()

def test_ptau_beacon_creates_new_file(tmp_path):
    ptau = PTau(working_dir=tmp_path)
    ptau.start()
    ptau_file_start = tmp_path / ptau.ptau_file
    assert ptau_file_start.exists()
    ptau.contribute()
    ptau_file_contrib = tmp_path / ptau.ptau_file
    assert ptau_file_start != ptau_file_contrib 
    assert ptau_file_contrib.exists()
    ptau.beacon()
    ptau_file_beacon = tmp_path / ptau.ptau_file
    assert ptau_file_beacon != ptau_file_contrib
    assert ptau_file_beacon.exists()

def test_ptau_phase2_creates_new_file(tmp_path):
    ptau = PTau(working_dir=tmp_path)
    ptau.start()
    ptau_file_start = tmp_path / ptau.ptau_file
    assert ptau_file_start.exists()
    ptau.contribute()
    ptau_file_contrib = tmp_path / ptau.ptau_file
    assert ptau_file_start != ptau_file_contrib 
    assert ptau_file_contrib.exists()
    ptau.beacon()
    ptau_file_beacon = tmp_path / ptau.ptau_file
    assert ptau_file_beacon != ptau_file_contrib
    assert ptau_file_beacon.exists()
    ptau.prep_phase2()
    ptau_file_phase2 = tmp_path / ptau.ptau_file
    assert ptau_file_phase2 != ptau_file_beacon
    assert ptau_file_phase2.exists()

def test_verify_fails_if_file_changed(tmp_path):
    ptau = PTau(working_dir=tmp_path)
    ptau.start()
    ptau_file_start = tmp_path / ptau.ptau_file
    assert ptau_file_start.exists()
    ptau.contribute()
    ptau_file_contrib = tmp_path / ptau.ptau_file
    assert ptau_file_start != ptau_file_contrib 
    assert ptau_file_contrib.exists()
    with ptau_file_contrib.open("w") as f:
        f.write('asdjfakjsfk')
    assert ptau.verify() == 1