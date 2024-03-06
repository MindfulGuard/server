class Middleware:
    def update_token_information(self):
        from mindfulguard.middleware import UpdateTokenInformationMiddleware
        obj = UpdateTokenInformationMiddleware()
        return obj