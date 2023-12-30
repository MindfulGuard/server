from mindfulguard.classes.user.base import UserBase
from mindfulguard.user.settings.delete_account import UserSettingsDeleteAccount
from mindfulguard.user.settings.one_time_codes_update import UserSettingsUpdateOneTimeCodes
from mindfulguard.user.settings.secret_string_update import UserSettingsUpdateSecretString


class UserSettings:
    def update_one_time_codes(self) -> UserSettingsUpdateOneTimeCodes:
        obj: UserBase = UserSettingsUpdateOneTimeCodes()
        return obj
    
    def update_secret_string(self):
        obj: UserBase = UserSettingsUpdateSecretString()
        return obj
    
    def delete_account(self):
        obj: UserBase = UserSettingsDeleteAccount()
        return obj