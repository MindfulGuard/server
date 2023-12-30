from mindfulguard.middleware.update_token_information import UpdateTokenInformationMiddleware

class Middleware:
    def update_token_information(self):
        obj = UpdateTokenInformationMiddleware()
        return obj