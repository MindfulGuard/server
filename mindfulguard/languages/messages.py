from typing import Any

from mindfulguard.languages.localization import Localization

class Messages:
    def __init__(self) -> None:
        """
        Initializes an instance of Messages class.
        """
        ...

    def get(self, key: str) -> dict[str, Any]:
        """
        Retrieves translations for a given key.

        Args:
            key (str): The key for which translations are required.

        Returns:
            dict[str, Any]: A dictionary containing translations in different locales.
                Example: {"en": "Message", "ru": "Сообщение", ...}
        """
        translations = {}
        localization = Localization()

        for locale in localization.locales:
            try:
                localization = Localization(locale)
                lang = localization.of()
                translation = getattr(lang, key)
                translations[locale] = translation
            except NotImplementedError:
                translations[locale] = f"No translation found for {key} in {locale} localization."

        return translations
