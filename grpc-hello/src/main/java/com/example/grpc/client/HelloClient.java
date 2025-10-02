package com.example.grpc.client;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.stub.StreamObserver;
import com.example.grpc.HelloRequest;
import com.example.grpc.HelloResponse;
import com.example.grpc.HelloServiceGrpc;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class HelloClient {
    private final ManagedChannel channel;
    private final HelloServiceGrpc.HelloServiceBlockingStub blockingStub;
    private final HelloServiceGrpc.HelloServiceStub asyncStub;

    public HelloClient(String host, int port) {
        this.channel = ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext()
                .build();
        this.blockingStub = HelloServiceGrpc.newBlockingStub(channel);
        this.asyncStub = HelloServiceGrpc.newStub(channel);
    }

    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }

    // Unary RPC call
    public void sayHello(String name) {
        System.out.println("=== Unary RPC Call ===");
        System.out.println("Sending request for: " + name);

        HelloRequest request = HelloRequest.newBuilder().setName(name).build();
        HelloResponse response = blockingStub.sayHello(request);

        System.out.println("Received response: " + response.getMessage());
        System.out.println("Timestamp: " + response.getTimestamp());
        System.out.println();
    }

    // Server streaming RPC call
    public void streamHello(String name) throws InterruptedException {
        System.out.println("=== Server Streaming RPC Call ===");
        System.out.println("Starting streaming request for: " + name);

        HelloRequest request = HelloRequest.newBuilder().setName(name).build();
        CountDownLatch finishLatch = new CountDownLatch(1);

        StreamObserver<HelloResponse> responseObserver = new StreamObserver<HelloResponse>() {
            @Override
            public void onNext(HelloResponse response) {
                System.out.println("Received stream response: " + response.getMessage());
                System.out.println("Timestamp: " + response.getTimestamp());
            }

            @Override
            public void onError(Throwable t) {
                System.err.println("Stream error: " + t.getMessage());
                finishLatch.countDown();
            }

            @Override
            public void onCompleted() {
                System.out.println("Stream completed");
                finishLatch.countDown();
            }
        };

        asyncStub.streamHello(request, responseObserver);
        finishLatch.await(1, TimeUnit.MINUTES);
    }

    public static void main(String[] args) {
        HelloClient client = new HelloClient("localhost", 50051);

        try {
            // Test unary RPC
            client.sayHello("World");

            // Test streaming RPC
            client.streamHello("Streaming World");

        } catch (Exception e) {
            System.err.println("Client error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            try {
                client.shutdown();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}