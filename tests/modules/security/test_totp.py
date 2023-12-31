from mindfulguard.classes.security import Security


def test_totp():
    security = Security()
    totp1 = security.totp('')
    secret_code: str = totp1.generate_secret_code()
    totp2 = security.totp(secret_code)
    
    assert totp2.verify(totp2.get()) == True
