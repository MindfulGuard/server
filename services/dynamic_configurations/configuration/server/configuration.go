package server

import (
	"errors"
	"fmt"
	"os"

	"github.com/mindfulguard/server/dynamic_configurations/logger"
	"go.uber.org/zap"
)

const (
	envSecretIDName string = "CONSUL_SECRET_ID"
	envHostName     string = "CONSUL_HOST"
)

type EnvConfiguration struct {
	SecretID string
	Host     string
}

type ServerConfiguration struct {
	Env *EnvConfiguration
}

func getEnvConfiguration() *EnvConfiguration {
	logger.Logger.Info("Getting values of environment variables...")

	var secretID string = ""
	var host string = ""
	var errorMsg string = ""

	if val := os.Getenv(envSecretIDName); val == "" {
		errorMsg += fmt.Sprintf("Missing %s in environment variables!\n", envSecretIDName)
	} else {
		secretID = val
	}

	if val := os.Getenv(envHostName); val == "" {
		errorMsg += fmt.Sprintf("Missing %s in environment variables!\n", envHostName)
	} else {
		host = val
	}

	logger.Logger.Debug(
		"Environment variables data.",
		zap.String(envSecretIDName, secretID),
		zap.String(envHostName, host),
	)

	if errorMsg != "" {
		logger.Logger.Fatal("Error getting environment variables.", zap.Error(errors.New(errorMsg)))
	}

	logger.Logger.Info("Values of environment variables successfully obtained.")

	return &EnvConfiguration{
		SecretID: secretID,
		Host:     host,
	}
}

func NewServerConfiguration() *ServerConfiguration {
	logger.Logger.Info("Initializing the server configuration...")

	return &ServerConfiguration{
		Env: getEnvConfiguration(),
	}
}
