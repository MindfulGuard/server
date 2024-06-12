package keyvalue

import (
	"fmt"

	consapi "github.com/hashicorp/consul/api"
	"github.com/mindfulguard/server/dynamic_configurations/consul"
	"github.com/mindfulguard/server/dynamic_configurations/logger"
	"go.uber.org/zap"
)

type IConsulKV interface {
	Put(key string, value []byte) bool
	Get(key string) (string, []byte, error)
}

type ConsulKV struct {
	clientKV *consapi.KV
}

func (c *ConsulKV) Put(key string, value []byte) bool {
	logger.Logger.Debug("Inserting an item into the key-value storage...", zap.String("Key-value.", fmt.Sprintf("%s: %s", key, value)))

	p := &consapi.KVPair{Key: key, Value: value}
	_, err := c.clientKV.Put(p, nil)
	if err != nil {
		logger.Logger.Warn(
			"Failed to put item in kv storage!",
			zap.String("Key-value.", fmt.Sprintf("%s: %s", key, value)),
			zap.Error(err),
		)
		return false
	} else {
		logger.Logger.Debug("The item was successfully added to the key-value storage.")

		return true
	}
}

func (c *ConsulKV) Get(key string) (string, []byte, error) {
	logger.Logger.Debug(
		"Retrieving data from key-value storage...",
		zap.String("Key", key),
	)

	pair, _, err := c.clientKV.Get(key, nil)
	if err != nil {
		logger.Logger.Warn("Failed to retrieve data from key-value storage.", zap.Error(err))
		return "", nil, err
	} else {
		logger.Logger.Debug(
			"Data from key-value store successfully retrieved.",
			zap.String("Key-value", fmt.Sprintf("%s: %s", pair.Key, pair.Value)),
			zap.Error(err),
		)

		return pair.Key, pair.Value, nil
	}
}

func (c *ConsulKV) Delete(key string) bool {
	_, err := c.clientKV.Delete("", nil)
	if err != nil {
		
		return false
	} else {
		return true
	}
}

func NewConsulKV(client *consul.Consul) *ConsulKV {
	logger.Logger.Info("Initialization of \"consulKV\" structure...")

	return &ConsulKV{
		clientKV: client.Client.KV(),
	}
}
