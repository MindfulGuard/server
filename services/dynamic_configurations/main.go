package main

import (
	"flag"
	"fmt"

	server_config "github.com/mindfulguard/server/dynamic_configurations/configuration/server"
	"github.com/mindfulguard/server/dynamic_configurations/logger"
	"github.com/mindfulguard/server/dynamic_configurations/server"
	"go.uber.org/zap"
)

func main() {
	const port_ string = "9001"

	logLevel := flag.String(
		"LOG-LEVEL",
		logger.LOG_LEVEL_INFO,
		fmt.Sprintf(
			"Sets the log level (%s, %s, %s, %s, %s)",
			logger.LOG_LEVEL_DEBUG,
			logger.LOG_LEVEL_INFO,
			logger.LOG_LEVEL_WARNING,
			logger.LOG_LEVEL_ERROR,
			logger.LOG_LEVEL_FATAL,
		),
	)
	logOutputType := flag.Bool(
		"LOG-PRODUCTION",
		false,
		"Sets the type of logs. \"true\" is for production, \"false\" is for development (default \"false\")",
	)
	port := flag.String(
		"PORT",
		port_,
		"Set the port on which the server will run",
	)

	flag.Parse()

	logger.NewLogger(*logLevel, *logOutputType)

	serverConfig, errConfig := server_config.NewServerConfiguration()
	if errConfig != nil {
		zap.L().Fatal("Error getting environment variables.", zap.Error(errConfig))
	}

	server.NewServer(fmt.Sprintf(":%s", *port), serverConfig.Env)
}
