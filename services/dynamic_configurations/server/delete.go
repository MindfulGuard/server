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

func (s *server) Delete(ctx context.Context, in *pb.DeleteRequest) (*pb.DeleteResponse, error) {
	start := time.Now()
	timestamp := time.Now().UTC().Format(time.RFC3339)
	zap.L().Debug("Delete method called",
		zap.String("timestamp", timestamp),
		zap.String("key", in.Key))

	ctxWithTimeout, cancel := context.WithTimeout(ctx, time.Second)
	defer cancel()

	serviceResult, err := service.NewService(s.envConfig).Delete(ctxWithTimeout, in.Key)
	duration := time.Since(start).Milliseconds()

	if err != nil {
		zap.L().Debug("Service Delete method error",
			zap.Error(err),
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return nil, status.Error(codes.DeadlineExceeded, codes.DeadlineExceeded.String())
	}

	if serviceResult {
		zap.L().Debug("Delete method succeeded",
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return &pb.DeleteResponse{
			Timestamp:                 timestamp,
			ExecutionTimeMilliseconds: duration,
		}, status.Error(codes.OK, codes.OK.String())
	} else {
		zap.L().Debug("Delete method - key not found",
			zap.String("key", in.Key),
			zap.Int64("execution_time_ms", duration))
		return nil, status.Error(codes.NotFound, codes.NotFound.String())
	}
}
