package consul

import (
	consul_api "github.com/hashicorp/consul/api"
	server_configuration "github.com/mindfulguard/server/dynamic_configurations/configuration/server"
	"go.uber.org/zap"
)

type Consul struct {
	conf   *server_configuration.EnvConfiguration
	Client *consul_api.Client
}

func NewConsul(envConfig *server_configuration.EnvConfiguration) *Consul {
	zap.L().Info("Consul client initialization...")

	config := consul_api.DefaultConfig()
	config.Address = envConfig.Host
	config.Token = envConfig.SecretID

	client, err := consul_api.NewClient(config)
	if err != nil {
		zap.L().Error("Failed to initialize the client for Consul.", zap.Error(err))
	}

	zap.L().Info("Consul client successfully initialized.")

	return &Consul{
		conf:   envConfig,
		Client: client,
	}
}
