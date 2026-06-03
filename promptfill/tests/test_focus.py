from promptfill.focus import ReturnTarget


def test_return_target_roundtrip():
    target = ReturnTarget("mac_bundle", "com.example.app")
    encoded = target.encode()
    decoded = ReturnTarget.decode(encoded)
    assert decoded == target


def test_return_target_decode_invalid():
    assert ReturnTarget.decode("not-json") is None
    assert ReturnTarget.decode('{"kind":"unknown","value":"x"}') is None
