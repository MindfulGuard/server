from mindfulguard.utils import minutes_to_seconds


def check_minutes_to_seconds()->bool:
    return minutes_to_seconds(1) == 60

def test_other():
    __check_minutes_to_seconds = check_minutes_to_seconds()

    assert __check_minutes_to_seconds == True