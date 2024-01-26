from typing import Any
from mindfulguard.languages.package_reader import PackageReader

class Messages:
    def __init__(self):
        self.__message = PackageReader()

    @property
    def successfully(self) -> dict[str,Any]:
        return self.__message.get("successfully")

    @property
    def data_not_valid(self) -> dict[str,Any]:
        return self.__message.get("data_not_valid")

    @property
    def registration_not_allowed(self) -> dict[str,Any]:
        return self.__message.get("registration_not_allowed")

    @property
    def registration_was_successful(self) -> dict[str,Any]:
        return self.__message.get("registration_was_successful")
    
    @property
    def service_is_not_available(self) -> dict[str,Any]:
        return self.__message.get("service_is_not_available")

    @property
    def server_error(self) -> dict[str,Any]:
        return self.__message.get("server_error")

    @property
    def user_already_exists(self) -> dict[str,Any]:
        return self.__message.get("user_already_exists")

    @property
    def user_not_found(self) -> dict[str,Any]:
        return self.__message.get("user_not_found")

    @property
    def user_found(self) -> dict[str,Any]:
        return self.__message.get("user_found")

    @property
    def session_token_has_been_deleted(self) -> dict[str,Any]:
        return self.__message.get("session_token_has_been_deleted")

    @property
    def failed_to_delete_token(self) -> dict[str,Any]:
        return self.__message.get("failed_to_delete_token")

    @property
    def safe_was_successfully_created(self) -> dict[str,Any]:
        return self.__message.get("safe_was_successfully_created")

    @property
    def failed_to_create_a_safe(self) -> dict[str,Any]:
        return self.__message.get("failed_to_create_a_safe")

    @property
    def not_found(self) -> dict[str, Any]:
        return self.__message.get("not_found")

    @property
    def unauthorized(self) -> dict[str,Any]:
        return self.__message.get("unauthorized")

    @property
    def safe_was_successfully_updated(self) -> dict[str,Any]:
        return self.__message.get("safe_was_successfully_updated")

    @property
    def failed_to_update_safe(self) -> dict[str,Any]:
        return self.__message.get("failed_to_update_safe")

    @property
    def successful_login(self) -> dict[str,Any]:
        return self.__message.get("successful_login")

    @property
    def safe_has_been_successfully_deleted(self) -> dict[str,Any]:
        return self.__message.get("safe_has_been_successfully_deleted")

    @property
    def failed_to_delete_the_safe(self) -> dict[str,Any]:
        return self.__message.get("failed_to_delete_the_safe")

    @property
    def item_was_successfully_created(self) -> dict[str,Any]:
        return self.__message.get("item_was_successfully_created")

    @property
    def failed_to_create_item(self) -> dict[str,Any]:
        return self.__message.get("failed_to_create_item")

    @property
    def failed_to_update_the_item(self) -> dict[str,Any]:
        return self.__message.get("failed_to_update_the_item")

    @property
    def item_has_been_successfully_updated(self) -> dict[str,Any]:
        return self.__message.get("item_has_been_successfully_updated")

    @property
    def item_was_successfully_deleted(self) -> dict[str,Any]:
        return self.__message.get("item_was_successfully_deleted")

    @property
    def failed_to_delete_item(self) -> dict[str,Any]:
        return self.__message.get("failed_to_delete_item")

    @property
    def failed_to_update_favorite(self) -> dict[str,Any]:
        return self.__message.get("failed_to_update_favorite")

    @property
    def item_was_successfully_added_to_favorites(self) -> dict[str,Any]:
        return self.__message.get("item_was_successfully_added_to_favorites")

    @property
    def item_was_successfully_moved_to_safe(self) -> dict[str,Any]:
        return self.__message.get("item_was_successfully_moved_to_safe")

    @property
    def failed_to_move_item_to_safe(self) -> dict[str,Any]:
        return self.__message.get("failed_to_move_item_to_safe")

    @property
    def successfully_updated(self) -> dict[str,Any]:
        return self.__message.get("successfully_updated")

    @property
    def failed_to_update(self) -> dict[str,Any]:
        return self.__message.get("failed_to_update")

    @property
    def user_has_been_successfully_deleted(self) -> dict[str,Any]:
        return self.__message.get("user_has_been_successfully_deleted")

    @property
    def failed_to_delete_user(self) -> dict[str,Any]:
        return self.__message.get("failed_to_delete_user")

    @property
    def access_denied(self) -> dict[str,Any]:
        return self.__message.get("access_denied")

    @property
    def settings_have_been_successfully_updated(self) -> dict[str,Any]:
        return self.__message.get("settings_have_been_successfully_updated")

    @property
    def failed_to_update_settings(self) -> dict[str,Any]:
        return self.__message.get("failed_to_update_settings")
    
    @property
    def conflict(self) -> dict[str,Any]:
        return self.__message.get("conflict")