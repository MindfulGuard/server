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

func TestDynamicConfigurationsServicePut(t *testing.T) {
	// Set up a connection to the server
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	// Create a client instance
	client := pb.NewDynamicConfigurationsClient(conn)

	// Prepare Put request
	req := &pb.PutRequest{
		Key:   "test_key",
		Value: []byte("test_value"),
	}

	// Call Put RPC
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	resp, err := client.Put(ctx, req)
	if err != nil {
		t.Fatalf("Put failed: %v", err)
	}

	// Assert on response if needed
	if resp.Timestamp == "" || resp.ExecutionTimeMilliseconds <= 0 {
		t.Errorf("Unexpected response: %v", resp)
	}
}

func TestDynamicConfigurationsServiceGet(t *testing.T) {
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	req := &pb.GetRequest{
		Key: "test_key",
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	resp, err := client.Get(ctx, req)
	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}

	if resp.Timestamp == "" || resp.ExecutionTimeMilliseconds <= 0 || len(resp.Value) == 0 {
		t.Errorf("Unexpected response: %v", resp)
	}
}

func TestDynamicConfigurationsServiceGetList(t *testing.T) {
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	req := &pb.GetListRequest{
		Prefix: "test_prefix_that_does_not_exist",
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	resp, err := client.GetList(ctx, req)
	if err != nil {
		t.Fatalf("GetList failed: %v", err)
	}

	if resp.Timestamp == "" || resp.ExecutionTimeMilliseconds <= 0 {
		t.Errorf("Unexpected response: %v", resp)
	}

	// Check if the list is empty or not
	if len(resp.List) == 0 {
		fmt.Println("No items found with the prefix:", req.Prefix)
	} else {
		fmt.Printf("Received list: %v\n", resp.List)
	}
}

func TestDynamicConfigurationsServiceDelete(t *testing.T) {
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	req := &pb.DeleteRequest{
		Key: "test_key",
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	resp, err := client.Delete(ctx, req)
	if err != nil {
		t.Fatalf("Delete failed: %v", err)
	}

	if resp.Timestamp == "" || resp.ExecutionTimeMilliseconds <= 0 {
		t.Errorf("Unexpected response: %v", resp)
	}
}

func TestDynamicConfigurationsServiceDeleteTree(t *testing.T) {
	// Set up a connection to the server
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	// Create a client instance
	client := pb.NewDynamicConfigurationsClient(conn)

	// Prepare data by putting some keys with the specified prefix
	for i := 1; i <= 5; i++ {
		key := fmt.Sprintf("test_prefix_%d", i)
		value := fmt.Sprintf("value_%d", i)
		putReq := &pb.PutRequest{
			Key:   key,
			Value: []byte(value),
		}

		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		defer cancel()

		_, err := client.Put(ctx, putReq)
		if err != nil {
			t.Fatalf("Put failed: %v", err)
		}
	}

	// Delete keys with the specified prefix
	req := &pb.DeleteTreeRequest{
		Prefix: "test_prefix",
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	resp, err := client.DeleteTree(ctx, req)
	if err != nil {
		t.Fatalf("DeleteTree failed: %v", err)
	}

	if resp.Timestamp == "" || resp.ExecutionTimeMilliseconds <= 0 || resp.Deleted <= 0 {
		t.Errorf("Unexpected response: %v", resp)
	}
}
