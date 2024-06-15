// +build servertests

package grpctest

import (
	"context"
	"fmt"
	"testing"
	"time"

	pb "github.com/mindfulguard/server/dynamic_configurations/grpc/gen"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

const (
	address = "localhost:9002"
)

func cleanStorage(t *testing.T) {
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// DeleteTree operation
	_, errDeleteTree := client.DeleteTree(ctx, &pb.DeleteTreeRequest{
		Prefix: "",
	})

	if statusCode, ok := status.FromError(errDeleteTree); !ok {
		t.Errorf("Record deletion error. Expected: %v, got: %v", codes.OK.String(), statusCode.Code().String())
	}
}

func TestDynamicConfigurationsServicePutAndGet(t *testing.T) {
	defer cleanStorage(t)

	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	// Test data
	key := "test_key_put_and_get"
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
	defer cleanStorage(t)

	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	// Test data
	prefix := "test_prefix_get_list"

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

func TestDynamicConfigurationsServicePutAndDelete(t *testing.T) {
	defer cleanStorage(t)

	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	// Test data
	key := "test_prefix_put_and_delete"

	// Put multiple keys with the prefix
	value := []byte("value_hello")

	putReq := &pb.PutRequest{
		Key:   key,
		Value: value,
	}

	ctxPut, cancelPut := context.WithTimeout(context.Background(), time.Second)
	defer cancelPut()

	_, errPut := client.Put(ctxPut, putReq)
	if errPut != nil {
		t.Fatalf("Put failed: %v", err)
	}

	// Context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// DeleteTree operation
	_, errDelete := client.Delete(ctx, &pb.DeleteRequest{
		Key: key,
	})
	if errDelete != nil {
		t.Fatalf("DeleteTree failed: %v", errDelete)
	}

	// Assert on the received list
	if statusCode, ok := status.FromError(errDelete); !ok {
		t.Errorf("Record deletion error. Expected: %v, got: %v", codes.OK.String(), statusCode.Code().String())
	}

	_, errDeleteNotFound := client.Delete(ctx, &pb.DeleteRequest{
		Key: "temp_key_123465",
	})

	if statusCode, _ := status.FromError(errDeleteNotFound); codes.NotFound.String() != statusCode.Code().String() {
		t.Errorf("Record deletion error. Expected: %v, got: %v", codes.NotFound.String(), statusCode.Code().String())
	}
}

func TestDynamicConfigurationsServicePutAndDeleteTree(t *testing.T) {
	defer cleanStorage(t)

	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		t.Fatalf("Failed to dial server: %v", err)
	}
	defer conn.Close()

	client := pb.NewDynamicConfigurationsClient(conn)

	// Test data
	prefix := "test_prefix_put_and_delete_tree"

	// Put multiple keys with the prefix
	for i := 1; i <= 3; i++ {
		key := fmt.Sprintf("%s/%d", prefix, i)
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

	// Context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// DeleteTree operation
	deleteTreeResp, err := client.DeleteTree(ctx, &pb.DeleteTreeRequest{
		Prefix: prefix,
	})
	if err != nil {
		t.Fatalf("DeleteTree failed: %v", err)
	}

	// Assert on the received list
	expectedNumItems := 3
	if deleteTreeResp.Deleted != int32(expectedNumItems) {
		t.Errorf("Expected %d items with prefix %s, but got %d", expectedNumItems, prefix, deleteTreeResp.Deleted)
	}
}
