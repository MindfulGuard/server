// +build unittests

package server

import (
	"os"
	"testing"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// set up a logger for testing
func setupLogger() {
	config := zap.NewDevelopmentConfig()
	config.EncoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder
	logger, _ := config.Build()
	zap.ReplaceGlobals(logger)
}

func TestGetEnvConfiguration(t *testing.T) {
	setupLogger()

	t.Run("MissingBothEnvVariables", func(t *testing.T) {
		os.Unsetenv(envSecretIDName)
		os.Unsetenv(envHostName)

		_, err := getEnvConfiguration()
		if err == nil {
			t.Errorf("Expected error when both environment variables are missing, but got none")
		}
	})

	t.Run("MissingSecretID", func(t *testing.T) {
		os.Unsetenv(envSecretIDName)
		os.Setenv(envHostName, "test-host")

		_, err := getEnvConfiguration()
		if err == nil {
			t.Errorf("Expected error when SecretID environment variable is missing, but got none")
		}
	})

	t.Run("MissingHost", func(t *testing.T) {
		os.Setenv(envSecretIDName, "test-secret-id")
		os.Unsetenv(envHostName)

		_, err := getEnvConfiguration()
		if err == nil {
			t.Errorf("Expected error when Host environment variable is missing, but got none")
		}
	})

	t.Run("AllEnvVariablesPresent", func(t *testing.T) {
		os.Setenv(envSecretIDName, "test-secret-id")
		os.Setenv(envHostName, "test-host")

		envConfig, err := getEnvConfiguration()
		if err != nil {
			t.Errorf("Did not expect error when all environment variables are present, but got: %v", err)
		}

		if envConfig.SecretID != "test-secret-id" {
			t.Errorf("Expected SecretID to be 'test-secret-id', got '%s'", envConfig.SecretID)
		}

		if envConfig.Host != "test-host" {
			t.Errorf("Expected Host to be 'test-host', got '%s'", envConfig.Host)
		}
	})
}
