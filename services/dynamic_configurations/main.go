package main

import (
	"flag"
	"fmt"

	//server_configuration "github.com/mindfulguard/server/dynamic_configurations/configuration/server"
	"github.com/mindfulguard/server/dynamic_configurations/logger"
)

func main() {
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
	flag.Parse()

	logger.NewLogger(*logLevel)

	//serv_cfg := server_configuration.NewServerConfiguration()
}
