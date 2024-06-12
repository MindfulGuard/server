package consul

import (
	consul_api "github.com/hashicorp/consul/api"
	server_configuration "github.com/mindfulguard/server/dynamic_configurations/configuration/server"
	"github.com/mindfulguard/server/dynamic_configurations/logger"
)

type Consul struct {
	conf   *server_configuration.EnvConfiguration
	Client *consul_api.Client
}

func NewConsul(envConfig *server_configuration.EnvConfiguration) *Consul {
	logger.Logger.Info("Consul client initialization...")

	config := consul_api.DefaultConfig()
	config.Address = envConfig.Host
	config.Token = envConfig.SecretID

	client, err := consul_api.NewClient(config)
	if err != nil {
		logger.Logger.Error("Failed to initialize the client for Consul.", err)
	}

	logger.Logger.Info("Consul client successfully initialized.")

	return &Consul{
		conf:   envConfig,
		Client: client,
	}
}
