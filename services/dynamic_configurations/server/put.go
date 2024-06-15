package server

import (
	"context"
	"time"

	pb "github.com/mindfulguard/server/dynamic_configurations/grpc/gen"
	"github.com/mindfulguard/server/dynamic_configurations/lib/strings"
	"github.com/mindfulguard/server/dynamic_configurations/service"
	"go.uber.org/zap"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func (s *server) Put(ctx context.Context, in *pb.PutRequest) (*pb.PutResponse, error) {
	start := time.Now()
	timestamp := time.Now().UTC().Format(time.RFC3339)
	zap.L().Debug("Put method called",
		zap.String("timestamp", timestamp),
		zap.String("key", in.Key),
		zap.Binary("value", in.Value))

	ctxWithTimeout, cancel := context.WithTimeout(ctx, time.Millisecond*500)
	defer cancel()

	if strings.IsEmptyString(in.Key) {
		duration := time.Since(start).Milliseconds()
		zap.L().Debug("Empty key provided",
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return &pb.PutResponse{
			Timestamp:                 timestamp,
			ExecutionTimeMilliseconds: duration,
		}, status.Error(codes.InvalidArgument, codes.InvalidArgument.String())
	}

	serviceResult, err := service.NewService(s.envConfig).Put(ctxWithTimeout, in.Key, in.Value)
	duration := time.Since(start).Milliseconds()

	if err != nil {
		zap.L().Debug("Service Put method error",
			zap.Error(err),
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return nil, status.Error(codes.DeadlineExceeded, codes.DeadlineExceeded.String())
	}

	if !serviceResult {
		zap.L().Debug("Service Put method failed precondition",
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return nil, status.Error(codes.FailedPrecondition, codes.FailedPrecondition.String())
	}

	zap.L().Debug("Put method succeeded",
		zap.String("key", in.Key),
		zap.Int64("execution_time_ms", duration))
	return &pb.PutResponse{
		Timestamp:                 timestamp,
		ExecutionTimeMilliseconds: duration,
	}, status.Error(codes.OK, codes.OK.String())
}
