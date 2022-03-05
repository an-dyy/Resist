from resist import __version__, version


def test_version():
    assert __version__ == '0.1.0-alpha'

    assert version.major == 0
    assert version.minor == 1
    assert version.patch == 0
    assert version.id == "alpha"
