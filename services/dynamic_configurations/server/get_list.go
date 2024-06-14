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

func (s *server) GetList(ctx context.Context, in *pb.GetListRequest) (*pb.GetListResponse, error) {
	start := time.Now()
	timestamp := time.Now().UTC().Format(time.RFC3339)
	zap.L().Debug("GetList method called",
		zap.String("timestamp", timestamp),
		zap.String("prefix", in.Prefix))

	ctxWithTimeout, cancel := context.WithTimeout(ctx, time.Second)
	defer cancel()

	serviceResult, err := service.NewService(s.envConfig).GetList(ctxWithTimeout, in.Prefix)
	duration := time.Since(start).Milliseconds()

	if err != nil {
		zap.L().Debug("Service GetList method error",
			zap.Error(err),
			zap.String("prefix", in.Prefix),
			zap.Int64("execution_time_ms", duration))
		return nil, status.Error(codes.DeadlineExceeded, codes.DeadlineExceeded.String())
	}

	zap.L().Debug("GetList method succeeded",
		zap.String("prefix", in.Prefix),
		zap.Int64("execution_time_ms", duration),
		zap.Int("result_count", len(serviceResult)))
	return &pb.GetListResponse{
		Timestamp:                 timestamp,
		ExecutionTimeMilliseconds: duration,
		List:                      serviceResult,
	}, status.Error(codes.OK, codes.OK.String())
}
