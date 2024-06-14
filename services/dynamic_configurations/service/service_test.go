// +build unittests

package service

import (
	"context"
	"fmt"
	"testing"
	"time"

	"github.com/hashicorp/consul/api"
	"github.com/mindfulguard/server/dynamic_configurations/configuration/server"
	"github.com/mindfulguard/server/dynamic_configurations/consul"
	keyvalue "github.com/mindfulguard/server/dynamic_configurations/consul/key_value"
)

func setupTestService(t *testing.T) *Service {
	conf, errServConfig := server.NewServerConfiguration()
	if errServConfig != nil {
		t.Error(errServConfig)
	}

	client := consul.NewConsul(conf.Env)

	consulKV := keyvalue.NewConsulKV(client)
	svc := &Service{
		consulKV: consulKV,
	}

	waitForConsul(t, client.Client)

	return svc
}

func waitForConsul(t *testing.T, client *api.Client) {
	timeout := time.After(30 * time.Second)
	tick := time.Tick(500 * time.Millisecond)
	for {
		select {
		case <-timeout:
			t.Fatalf("Timed out waiting for Consul to be available")
		case <-tick:
			if leader, err := client.Status().Leader(); err == nil && leader != "" {
				fmt.Println("Consul is ready")
				return
			}
		}
	}
}

func TestServicePutGetDelete(t *testing.T) {
	svc := setupTestService(t)
	defer svc.consulKV.DeleteTree("") // Clean up after the test

	key := "test_key"
	value := []byte("test_value")

	// Test Put
	ctx := context.Background()
	result, err := svc.Put(ctx, key, value)
	if err != nil {
		t.Fatalf("Put returned error: %v", err)
	}
	if !result {
		t.Error("Put returned false, expected true")
	}

	// Test Get
	gotValue, err := svc.Get(ctx, key)
	if err != nil {
		t.Fatalf("Get returned error: %v", err)
	}
	if string(gotValue) != string(value) {
		t.Errorf("Get returned value %s, expected %s", gotValue, value)
	}

	// Test Delete
	result, err = svc.Delete(ctx, key)
	if err != nil {
		t.Fatalf("Delete returned error: %v", err)
	}
	if !result {
		t.Error("Delete returned false, expected true")
	}
}

func TestServiceGetList(t *testing.T) {
	svc := setupTestService(t)
	defer svc.consulKV.DeleteTree("") // Clean up after the test

	prefix := "test_prefix"

	// Put some data first
	key1 := prefix + "/key1"
	key2 := prefix + "/key2"
	value1 := []byte("value1")
	value2 := []byte("value2")

	ctx := context.Background()
	if _, err := svc.Put(ctx, key1, value1); err != nil {
		t.Fatalf("Error putting test data: %v", err)
	}
	if _, err := svc.Put(ctx, key2, value2); err != nil {
		t.Fatalf("Error putting test data: %v", err)
	}

	// Test GetList
	keys, err := svc.GetList(ctx, prefix)
	if err != nil {
		t.Fatalf("GetList returned error: %v", err)
	}
	if len(keys) != 2 || !(keys[0] == key1 || keys[0] == key2) || !(keys[1] == key1 || keys[1] == key2) {
		t.Errorf("GetList returned keys %v, expected [%s, %s]", keys, key1, key2)
	}
}

func TestServiceDeleteTree(t *testing.T) {
	svc := setupTestService(t)
	defer svc.consulKV.DeleteTree("") // Clean up after the test

	prefix := "test_prefix"

	// Put some data first
	key1 := prefix + "/key1"
	key2 := prefix + "/key2"
	value1 := []byte("value1")
	value2 := []byte("value2")

	ctx := context.Background()
	if _, err := svc.Put(ctx, key1, value1); err != nil {
		t.Fatalf("Error putting test data: %v", err)
	}
	if _, err := svc.Put(ctx, key2, value2); err != nil {
		t.Fatalf("Error putting test data: %v", err)
	}

	// Test DeleteTree
	result, _, err := svc.DeleteTree(ctx, prefix)
	if err != nil {
		t.Fatalf("DeleteTree returned error: %v", err)
	}
	if !result {
		t.Error("DeleteTree returned false, expected true")
	}
}
