class Middleware:
    def update_token_information(self):
        from mindfulguard.middleware.update_token_information import UpdateTokenInformationMiddleware
        obj = UpdateTokenInformationMiddleware()
        return obj