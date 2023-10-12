from mindfulguard.core.security.totp import NUMBER_OF_BACKUP_CODES, Totp


def totp():
    creator = Totp("")
    secret_code:str = creator.generate_secret_code()
    backup_codes:list[int] = creator.generate_backup_codes(NUMBER_OF_BACKUP_CODES)
    length_items:bool = False

    for item in backup_codes:
        if len(str(item)) == 6:
            length_items = True

    verifier = Totp(secret_code)
    one_time_code:str = verifier.get()
    verif:bool = verifier.verify(one_time_code)

    return (
        len(secret_code),
        len(backup_codes),
        length_items,
        len(one_time_code),
        verif
        )

def test_totp():
    __totp = totp()
    totp_secret_code_length:int = __totp[0]
    totp_backup_codes_length:int = __totp[1]
    totp_length_items:bool = __totp[2]
    totp_one_time_code_length:int = __totp[3]
    totp_is_confirmed:bool = __totp[4]

    assert totp_secret_code_length == 32, totp_secret_code_length
    assert totp_backup_codes_length == 5, totp_backup_codes_length #six backup codes
    assert totp_length_items == True, totp_length_items
    assert totp_one_time_code_length == 6, totp_one_time_code_length
    assert totp_is_confirmed == True, totp_is_confirmed
    