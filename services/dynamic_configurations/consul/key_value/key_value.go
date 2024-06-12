package keyvalue

import (
	consapi "github.com/hashicorp/consul/api"
	"github.com/mindfulguard/server/dynamic_configurations/consul"
	"github.com/mindfulguard/server/dynamic_configurations/logger"
	"go.uber.org/zap"
)

type IConsulKV interface {
	Put(key string, value []byte) bool
	Get(key string) (string, []byte, error)
	Keys(prefix string) ([]string, error)
	Delete(key string) bool
	DeleteTree(prefix string) bool
}

type ConsulKV struct {
	clientKV *consapi.KV
}

func (c *ConsulKV) Put(key string, value []byte) bool {
	logger.Logger.Debug(
		"Inserting an item into the key-value storage...",
		zap.String("key", key),
		zap.Binary("value", value),
	)

	p := &consapi.KVPair{Key: key, Value: value}
	_, err := c.clientKV.Put(p, nil)
	if err != nil {
		logger.Logger.Info(
			"Failed to put item in kv storage!",
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
		zap.String("key", key),
	)

	pair, _, err := c.clientKV.Get(key, nil)
	if err != nil {
		logger.Logger.Info("Failed to retrieve data from key-value storage.", zap.Error(err))
		return "", nil, err
	} else {
		logger.Logger.Debug(
			"Data from key-value store successfully retrieved.",
			zap.String("key", pair.Key),
			zap.Binary("value", pair.Value),
			zap.Error(err),
		)

		return pair.Key, pair.Value, nil
	}
}

func (c *ConsulKV) Keys(prefix string) ([]string, error) {
	logger.Logger.Debug(
		"Getting keys by prefix...",
		zap.String("prefix", prefix),
	)

	data, _, err := c.clientKV.Keys(prefix, "", nil)

	if err != nil {
		logger.Logger.Info("Failed to retrieve keys by prefix.", zap.Error(err))
		return nil, err
	} else {
		logger.Logger.Debug(
			"The keys were successfully received",
			zap.String("prefix", prefix),
			zap.Any("keys", data),
		)
		return data, nil
	}
}

func (c *ConsulKV) List(prefix string) (consapi.KVPairs, error) {
	logger.Logger.Debug("Retrieving the list of key-values...", zap.String("prefix", prefix))

	data, _, err := c.clientKV.List(prefix, nil)

	if err != nil {
		logger.Logger.Info("Failed to get the list of key-values!", zap.Error(err))
		return nil, err
	} else {
		logger.Logger.Debug("The list of key-values was successfully obtained.", zap.Any("data", data))
		return data, nil
	}
}

func (c *ConsulKV) Delete(key string) bool {
	logger.Logger.Debug("Deleting data from key-value storage...", zap.String("key", key))

	_, err := c.clientKV.Delete(key, nil)
	if err != nil {
		logger.Logger.Info("Failed to delete a value by key!", zap.Error(err))
		return false
	} else {
		logger.Logger.Debug("Value successfully deleted by key.")
		return true
	}
}

func (c *ConsulKV) DeleteTree(prefix string) bool {
	logger.Logger.Debug("Deleting data from key-value storage...", zap.String("prefix", prefix))

	_, err := c.clientKV.DeleteTree(prefix, nil)
	if err != nil {
		logger.Logger.Info("Failed to delete a value by prefix!", zap.Error(err))
		return false
	} else {
		logger.Logger.Debug("Values successfully deleted by prefix.")
		return true
	}
}

func NewConsulKV(client *consul.Consul) *ConsulKV {
	logger.Logger.Info("Initialization of \"ConsulKV\" structure...")

	return &ConsulKV{
		clientKV: client.Client.KV(),
	}
}
