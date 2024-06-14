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

func (s *server) Get(ctx context.Context, in *pb.GetRequest) (*pb.GetResponse, error) {
	start := time.Now()
	timestamp := time.Now().UTC().Format(time.RFC3339)
	zap.L().Debug("Get method called",
		zap.String("timestamp", timestamp),
		zap.String("key", in.Key))

	ctxWithTimeout, cancel := context.WithTimeout(ctx, time.Millisecond*500)
	defer cancel()

	if strings.IsEmptyString(in.Key) {
		duration := time.Since(start).Milliseconds()
		zap.L().Debug("Empty key provided",
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return &pb.GetResponse{
			Timestamp:                 timestamp,
			ExecutionTimeMilliseconds: duration,
		}, status.Error(codes.InvalidArgument, codes.InvalidArgument.String())
	}

	serviceResult, err := service.NewService(s.envConfig).Get(ctxWithTimeout, in.Key)
	duration := time.Since(start).Milliseconds()

	if err != nil {
		zap.L().Debug("Service Get method error",
			zap.Error(err),
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return nil, status.Error(codes.DeadlineExceeded, codes.DeadlineExceeded.String())
	}

	zap.L().Debug("Get method succeeded",
		zap.String("key", in.Key),
		zap.Binary("value", serviceResult),
		zap.Int64("execution_time_ms", duration))
	return &pb.GetResponse{
		Timestamp:                 timestamp,
		ExecutionTimeMilliseconds: duration,
		Value:                     serviceResult,
	}, status.Error(codes.OK, codes.OK.String())
}
