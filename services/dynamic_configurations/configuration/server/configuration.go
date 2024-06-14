package server

import (
	"errors"
	"fmt"
	"os"

	"go.uber.org/zap"
)

const (
	envSecretIDName string = "DYNAMIC_CONFIGURATIONS_CONSUL_SECRET_ID"
	envHostName     string = "DYNAMIC_CONFIGURATIONS_CONSUL_HOST"
)

type EnvConfiguration struct {
	SecretID string
	Host     string
}

type ServerConfiguration struct {
	Env *EnvConfiguration
}

func getEnvConfiguration() (*EnvConfiguration, error) {
	zap.L().Info("Getting values of environment variables...")

	var secretID string
	var host string
	var errorMsg string

	if val := os.Getenv(envSecretIDName); val == "" {
		errorMsg += fmt.Sprintf("Missing %s in environment variables!", envSecretIDName)
	} else {
		secretID = val
	}

	if val := os.Getenv(envHostName); val == "" {
		errorMsg += fmt.Sprintf(" Missing %s in environment variables!", envHostName)
	} else {
		host = val
	}

	zap.L().Debug(
		"Environment variables data.",
		zap.String(envSecretIDName, secretID),
		zap.String(envHostName, host),
	)

	if errorMsg != "" {
		return nil, errors.New(errorMsg)
	}

	zap.L().Info("Values of environment variables successfully obtained.")

	return &EnvConfiguration{
		SecretID: secretID,
		Host:     host,
	}, nil
}

func NewServerConfiguration() (*ServerConfiguration, error) {
	zap.L().Info("Initializing the server configuration...")

	envConfig, err := getEnvConfiguration()
	if err != nil {
		return nil, err
	}

	return &ServerConfiguration{
		Env: envConfig,
	}, nil
}
