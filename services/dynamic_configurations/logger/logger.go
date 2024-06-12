package logger

import (
	"fmt"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

type logger struct {
	*zap.Logger
}

const (
	LOG_LEVEL_DEBUG   string = "DEBUG"
	LOG_LEVEL_INFO    string = "INFO"
	LOG_LEVEL_WARNING string = "WARNING"
	LOG_LEVEL_ERROR   string = "ERROR"
	LOG_LEVEL_FATAL   string = "FATAL"
)

var (
	Logger *logger
)

func NewLogger(logLevel string) {
	var level zapcore.Level = zapcore.DebugLevel

	switch logLevel {
	case LOG_LEVEL_DEBUG:
		level = zapcore.DebugLevel
	case LOG_LEVEL_INFO:
		level = zapcore.InfoLevel
	case LOG_LEVEL_WARNING:
		level = zapcore.WarnLevel
	case LOG_LEVEL_ERROR:
		level = zapcore.ErrorLevel
	case LOG_LEVEL_FATAL:
		level = zapcore.FatalLevel
	default:
		panic(fmt.Sprintf(
			"There is no such logging level: %s. Available levels: %s, %s, %s, %s, %s.",
			logLevel,
			LOG_LEVEL_DEBUG,
			LOG_LEVEL_INFO,
			LOG_LEVEL_WARNING,
			LOG_LEVEL_ERROR,
			LOG_LEVEL_FATAL,
		))
	}

	config := zap.NewDevelopmentConfig()
	config.EncoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder
	config.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	config.Level = zap.NewAtomicLevelAt(level)

	logger_, err := config.Build()
	if err != nil {
		panic(err)
	}

	Logger = &logger{logger_}

	Logger.Info("Logger initialized.")
}
