from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests"
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency"
)