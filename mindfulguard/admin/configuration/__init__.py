from mindfulguard.admin.configuration.get import AdminConfigurationGet
from mindfulguard.admin.configuration.update import AdminConfigurationUpdate


class AdminConfiguration:
    def get(self) -> AdminConfigurationGet:
        return AdminConfigurationGet()
    
    def update(self) -> AdminConfigurationUpdate:
        return AdminConfigurationUpdate()