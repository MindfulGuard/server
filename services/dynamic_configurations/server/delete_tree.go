package server

import (
	"context"
	"time"

	pb "github.com/mindfulguard/server/dynamic_configurations/grpc/gen"
	"github.com/mindfulguard/server/dynamic_configurations/service"
	"go.uber.org/zap"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func (s *server) DeleteTree(ctx context.Context, in *pb.DeleteTreeRequest) (*pb.DeleteTreeResponse, error) {
	start := time.Now()
	timestamp := time.Now().UTC().Format(time.RFC3339)
	zap.L().Debug("DeleteTree method called",
		zap.String("timestamp", timestamp),
		zap.String("prefix", in.Prefix))

	ctxWithTimeout, cancel := context.WithTimeout(ctx, time.Second)
	defer cancel()

	serviceResult, deleted, err := service.NewService(s.envConfig).DeleteTree(ctxWithTimeout, in.Prefix)
	duration := time.Since(start).Milliseconds()

	if err != nil {
		zap.L().Debug("Service DeleteTree method error",
			zap.Error(err),
			zap.String("prefix", in.Prefix),
			zap.Int64("execution_time_ms", duration))
		return nil, status.Error(codes.DeadlineExceeded, codes.DeadlineExceeded.String())
	}

	if serviceResult && deleted > 0 {
		zap.L().Debug("DeleteTree method succeeded",
			zap.String("prefix", in.Prefix),
			zap.Int64("execution_time_ms", duration),
			zap.Int("deleted_count", deleted))
		return &pb.DeleteTreeResponse{
			Timestamp:                 timestamp,
			ExecutionTimeMilliseconds: duration,
			Deleted:                   int32(deleted),
		}, status.Error(codes.OK, codes.OK.String())
	} else {
		zap.L().Debug("DeleteTree method - prefix not found or no items deleted",
			zap.String("prefix", in.Prefix),
			zap.Int64("execution_time_ms", duration),
			zap.Int("deleted_count", deleted))
		return nil, status.Error(codes.NotFound, codes.NotFound.String())
	}
}
