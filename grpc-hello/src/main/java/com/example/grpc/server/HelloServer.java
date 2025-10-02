package com.example.grpc.server;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import com.example.grpc.HelloRequest;
import com.example.grpc.HelloResponse;
import com.example.grpc.HelloServiceGrpc;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.TimeUnit;

public class HelloServer {
    private final int port;
    private final Server server;

    public HelloServer(int port) {
        this.port = port;
        this.server = ServerBuilder.forPort(port)
                .addService(new HelloServiceImpl())
                .build();
    }

    public void start() throws IOException {
        server.start();
        System.out.println("Server started, listening on " + port);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.err.println("*** shutting down gRPC server since JVM is shutting down");
            try {
                HelloServer.this.stop();
            } catch (InterruptedException e) {
                e.printStackTrace(System.err);
            }
            System.err.println("*** server shut down");
        }));
    }

    public void stop() throws InterruptedException {
        if (server != null) {
            server.shutdown().awaitTermination(30, TimeUnit.SECONDS);
        }
    }

    public void blockUntilShutdown() throws InterruptedException {
        if (server != null) {
            server.awaitTermination();
        }
    }

    static class HelloServiceImpl extends HelloServiceGrpc.HelloServiceImplBase {

        @Override
        public void sayHello(HelloRequest request, StreamObserver<HelloResponse> responseObserver) {
            String greeting = "Hello, " + request.getName() + "!";
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);

            HelloResponse response = HelloResponse.newBuilder()
                    .setMessage(greeting)
                    .setTimestamp(timestamp)
                    .build();

            System.out.println("Sending response: " + greeting);
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        }

        @Override
        public void streamHello(HelloRequest request, StreamObserver<HelloResponse> responseObserver) {
            String name = request.getName();

            for (int i = 1; i <= 5; i++) {
                String greeting = "Hello " + name + " #" + i;
                String timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);

                HelloResponse response = HelloResponse.newBuilder()
                        .setMessage(greeting)
                        .setTimestamp(timestamp)
                        .build();

                responseObserver.onNext(response);

                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    responseObserver.onError(e);
                    return;
                }
            }
            responseObserver.onCompleted();
        }
    }

    public static void main(String[] args) throws Exception {
        HelloServer server = new HelloServer(50051);
        server.start();
        server.blockUntilShutdown();
    }
}