package service

import consul_key_value "github.com/mindfulguard/server/dynamic_configurations/consul/key_value"

type Services struct {
	consulKV *consul_key_value.ConsulKV
}

func NewServices(consulKV *consul_key_value.ConsulKV) *Services {
	return &Services{
		consulKV: consulKV,
	}
}
