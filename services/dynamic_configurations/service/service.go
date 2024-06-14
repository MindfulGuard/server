package service

import (
	"context"

	"github.com/mindfulguard/server/dynamic_configurations/configuration/server"
	"github.com/mindfulguard/server/dynamic_configurations/consul"
	consul_key_value "github.com/mindfulguard/server/dynamic_configurations/consul/key_value"
	"go.uber.org/zap"
)

type Service struct {
	consulKV *consul_key_value.ConsulKV
}

func (s *Service) Put(ctx context.Context, key string, value []byte) (bool, error) {
	zap.L().Debug("Adding an item...", zap.String("key", key), zap.Binary("value", value))

	resultCh := make(chan bool, 1)

	go func() {
		defer close(resultCh)

		resultCh <- s.consulKV.Put(key, value)
	}()

	select {
	case <-ctx.Done():
		ctxErr := ctx.Err()

		zap.L().Error("The waiting time for function Put execution has been exceeded!", zap.Error(ctxErr))

		return false, ctxErr
	case result := <-resultCh:
		zap.L().Debug("The add operation was successful.", zap.Bool("result", result))

		return result, nil
	}
}

func (s *Service) Get(ctx context.Context, key string) ([]byte, error) {
	zap.L().Debug("Obtaining data by key...", zap.String("key", key))

	type result struct {
		value []byte
		err   error
	}

	resultCh := make(chan result, 1)

	go func() {
		defer close(resultCh)

		_, value, err := s.consulKV.Get(key)
		resultCh <- result{value, err}
	}()

	select {
	case <-ctx.Done():
		ctxErr := ctx.Err()

		zap.L().Error("The waiting time for function Get execution has been exceeded!", zap.Error(ctxErr))

		return nil, ctxErr
	case res := <-resultCh:
		zap.L().Debug("The data retrieval operation was successful.", zap.Binary("key", res.value), zap.Error(res.err))

		return res.value, res.err
	}
}

func (s *Service) GetList(ctx context.Context, prefix string) ([]string, error) {
	zap.L().Debug("Getting the list of keys...", zap.String("prefix", prefix))

	type result struct {
		keys []string
		err  error
	}

	resultCh := make(chan result, 1)

	go func() {
		defer close(resultCh)

		keys, err := s.consulKV.Keys(prefix)
		resultCh <- result{keys, err}
	}()

	select {
	case <-ctx.Done():
		ctxErr := ctx.Err()

		zap.L().Error("The waiting time for function GetList execution has been exceeded!", zap.Error(ctxErr))

		return nil, ctxErr
	case res := <-resultCh:
		zap.L().Debug("The key list retrieval operation was successful.", zap.Any("key", res.keys), zap.Error(res.err))

		return res.keys, res.err
	}
}

func (s *Service) Delete(ctx context.Context, key string) (bool, error) {
	zap.L().Debug("Deleting an object by its key...", zap.String("key", key))

	resultCh := make(chan bool, 1)

	go func() {
		defer close(resultCh)

		resultCh <- s.consulKV.Delete(key)
	}()

	select {
	case <-ctx.Done():
		ctxErr := ctx.Err()

		zap.L().Error("The waiting time for function Delete execution has been exceeded!", zap.Error(ctxErr))

		return false, ctx.Err()
	case res := <-resultCh:
		zap.L().Debug("The operation to delete an element by key was successful.", zap.Bool("result", res))
		return res, nil
	}
}

func (s *Service) DeleteTree(ctx context.Context, prefix string) (bool, int, error) {
	zap.L().Debug("Starting deletion of objects by prefix...", zap.String("prefix", prefix))

	lenListFunc := func() (int, error) {
		list, err := s.GetList(ctx, "")
		if err != nil {
			return 0, err
		} else {
			return len(list), nil
		}
	}

	lenBefore, err := lenListFunc()
	if err != nil {
		zap.L().Error("Error occurred while retrieving list length before deletion", zap.Error(err))
		return false, lenBefore, err
	}
	zap.L().Debug("Initial list length retrieved", zap.Int("lengthBefore", lenBefore))

	resultCh := make(chan bool, 1)
	go func() {
		defer close(resultCh)
		resultCh <- s.consulKV.DeleteTree(prefix)
	}()

	select {
	case <-ctx.Done():
		ctxErr := ctx.Err()
		zap.L().Error("The waiting time for function DeleteTree execution has been exceeded!", zap.Error(ctxErr))
		return false, 0, ctx.Err()
	case res := <-resultCh:
		zap.L().Debug("Deletion of objects by prefix completed", zap.Bool("result", res))

		lenAfter, err := lenListFunc()
		if err != nil {
			zap.L().Error("Error occurred while retrieving list length after deletion", zap.Error(err))
			return false, lenAfter, err
		}
		zap.L().Debug("Final list length retrieved", zap.Int("lengthAfter", lenAfter))

		return res, lenBefore - lenAfter, nil
	}
}

func NewService(envConfig *server.EnvConfiguration) *Service {
	zap.L().Debug("Service initialization...")

	client := consul.NewConsul(envConfig)

	return &Service{
		consulKV: consul_key_value.NewConsulKV(client),
	}
}
