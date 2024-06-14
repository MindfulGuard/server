// +build servertests

package grpctest

import (
	"context"
	"fmt"
	"testing"
	"time"

	pb "github.com/mindfulguard/server/dynamic_configurations/grpc/gen"
	"google.golang.org/grpc"
)

const (
	address = "localhost:9002"
)

func TestDynamicConfigurationsServicePutAndGet(t *testing.T) {
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	// Test data
	key := "test_key"
	value := []byte("test_value")

	// Put request
	putReq := &pb.PutRequest{
		Key:   key,
		Value: value,
	}

	// Context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// Put operation
	_, err = client.Put(ctx, putReq)
	if err != nil {
		t.Fatalf("Put failed: %v", err)
	}

	// Get request
	getReq := &pb.GetRequest{
		Key: key,
	}

	// Get operation
	getResp, err := client.Get(ctx, getReq)
	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}

	// Assert on retrieved value
	if string(getResp.Value) != string(value) {
		t.Errorf("Expected value %s, got %s", value, getResp.Value)
	}
}

func TestDynamicConfigurationsServiceGetListWithPrefix(t *testing.T) {
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	// Test data
	prefix := "test_prefix"

	// Put multiple keys with the prefix
	for i := 1; i <= 3; i++ {
		key := fmt.Sprintf("%s_%d", prefix, i)
		value := []byte(fmt.Sprintf("value_%d", i))

		putReq := &pb.PutRequest{
			Key:   key,
			Value: value,
		}

		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		defer cancel()

		_, err := client.Put(ctx, putReq)
		if err != nil {
			t.Fatalf("Put failed: %v", err)
		}
	}

	// GetList request
	getListReq := &pb.GetListRequest{
		Prefix: prefix,
	}

	// Context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// GetList operation
	getListResp, err := client.GetList(ctx, getListReq)
	if err != nil {
		t.Fatalf("GetList failed: %v", err)
	}

	// Assert on the received list
	expectedNumItems := 3
	if len(getListResp.List) != expectedNumItems {
		t.Errorf("Expected %d items with prefix %s, but got %d", expectedNumItems, prefix, len(getListResp.List))
	}
}
