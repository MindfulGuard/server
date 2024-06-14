package keyvalue

import (
	consapi "github.com/hashicorp/consul/api"
	"github.com/mindfulguard/server/dynamic_configurations/consul"
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
	zap.L().Debug(
		"Inserting an item into the key-value storage...",
		zap.String("key", key),
		zap.ByteString("value", value),
	)

	p := &consapi.KVPair{Key: key, Value: value}
	_, err := c.clientKV.Put(p, nil)
	if err != nil {
		zap.L().Error(
			"Failed to put item in kv storage!",
			zap.Error(err),
		)
		return false
	} else {
		zap.L().Debug("The item was successfully added to the key-value storage.")

		return true
	}
}

func (c *ConsulKV) Get(key string) (string, []byte, error) {
	zap.L().Debug(
		"Retrieving data from key-value storage...",
		zap.String("key", key),
	)

	pair, _, err := c.clientKV.Get(key, nil)
	if err != nil {
		zap.L().Error("Failed to retrieve data from key-value storage.", zap.Error(err))
		return "", nil, err
	} else {
		var key string = ""
		var value []byte = nil

		if pair != nil {
			zap.L().Debug(
				"Data from key-value store successfully retrieved.",
				zap.String("key", pair.Key),
				zap.Binary("value", pair.Value),
				zap.Error(err),
			)
			key = pair.Key
			value = pair.Value
		}

		return key, value, nil
	}
}

func (c *ConsulKV) Keys(prefix string) ([]string, error) {
	zap.L().Debug(
		"Getting keys by prefix...",
		zap.String("prefix", prefix),
	)

	data, _, err := c.clientKV.Keys(prefix, "", nil)

	if err != nil {
		zap.L().Error("Failed to retrieve keys by prefix.", zap.Error(err))
		return nil, err
	} else {
		zap.L().Debug(
			"The keys were successfully received",
			zap.String("prefix", prefix),
			zap.Any("keys", data),
		)
		return data, nil
	}
}

func (c *ConsulKV) List(prefix string) (consapi.KVPairs, error) {
	zap.L().Debug("Retrieving the list of key-values...", zap.String("prefix", prefix))

	data, _, err := c.clientKV.List(prefix, nil)

	if err != nil {
		zap.L().Error("Failed to get the list of key-values!", zap.Error(err))
		return nil, err
	} else {
		zap.L().Debug("The list of key-values was successfully obtained.", zap.Any("data", data))
		return data, nil
	}
}

func (c *ConsulKV) Delete(key string) bool {
	zap.L().Debug("Deleting data from key-value storage...", zap.String("key", key))

	keyGetBefore, valueGetBefore, errGetBefore := c.Get(key)
	if (keyGetBefore == "" && valueGetBefore == nil) || errGetBefore != nil {
		if errGetBefore != nil {
			zap.L().Error("Failed to retrieve element!", zap.Error(errGetBefore))
		}
		zap.L().Debug("Failed to find an item by its key.", zap.String("keyBefore", keyGetBefore), zap.Binary("valueBefore", valueGetBefore))
		return false
	}

	_, err := c.clientKV.Delete(key, nil)
	if err != nil {
		zap.L().Error("Failed to delete a value by key!", zap.Error(err))
		return false
	} else {
		keyGetAfter, valueGetAfter, errGetAfter := c.Get(key)

		if errGetAfter != nil {
			zap.L().Error("Failed to retrieve element!", zap.Error(errGetAfter))
			return false
		}

		if keyGetAfter == "" && valueGetAfter == nil {
			zap.L().Debug("Value successfully deleted by key.", zap.String("keyAfter", keyGetAfter), zap.Binary("valueAfter", valueGetAfter))
			return true
		} else {
			zap.L().Debug("Failed to delete a value by key.", zap.String("keyAfter", keyGetAfter), zap.Binary("valueAfter", valueGetAfter))
			return false
		}
	}
}

func (c *ConsulKV) DeleteTree(prefix string) bool {
	zap.L().Debug("Deleting data from key-value storage...", zap.String("prefix", prefix))

	_, err := c.clientKV.DeleteTree(prefix, nil)

	if err != nil {
		zap.L().Error("Failed to delete a value by prefix!", zap.Error(err))
		return false
	} else {
		zap.L().Debug("Values successfully deleted by prefix.")
		return true
	}
}

func NewConsulKV(client *consul.Consul) *ConsulKV {
	zap.L().Info("Initialization of \"ConsulKV\" structure...")

	return &ConsulKV{
		clientKV: client.Client.KV(),
	}
}
