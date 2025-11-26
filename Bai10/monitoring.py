from prometheus_client import Counter, Histogram, CollectorRegistry, generate_latest

registry = CollectorRegistry()

REQUEST_COUNT = Counter(
    "http_request_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
    registry=registry
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Latency of HTTP requests",
    ["endpoint"],
    registry=registry
)
