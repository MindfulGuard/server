package server

import (
	"net"

	server_conf "github.com/mindfulguard/server/dynamic_configurations/configuration/server"
	pb "github.com/mindfulguard/server/dynamic_configurations/grpc/gen"
	"go.uber.org/zap"
	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedDynamicConfigurationsServer
	envConfig *server_conf.EnvConfiguration
}

func NewServer(port string, envConfig *server_conf.EnvConfiguration) {
	zap.L().Info("Trying to start the server...")
	lis, err := net.Listen("tcp", port)
	if err != nil {
		zap.L().Fatal("Failed to listen on port!", zap.String("port", port), zap.Error(err))
	}

	s := grpc.NewServer()
	pb.RegisterDynamicConfigurationsServer(s, &server{
		envConfig: envConfig,
	})
	zap.L().Info("gRPC server listening address", zap.String("address", lis.Addr().String()))
	if err := s.Serve(lis); err != nil {
		zap.L().Fatal("failed to serve", zap.Error(err))
	}
}
