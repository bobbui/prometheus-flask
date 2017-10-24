import time
from urllib.parse import urlparse, parse_qs

from flask import request
from flask.helpers import make_response
from prometheus_client import core, generate_latest, CONTENT_TYPE_LATEST, Gauge, Histogram, Counter
import flask
from prometheus.host import monitor_host_metrics


def monitor(app):
    def before_request():
        flask.g.start_time = time.time()
        http_concurrent_request_count.inc()
        content_length = request.content_length
        if (content_length):
            http_request_size_bytes.labels(request.method, request.path).observe(content_length)

    def after_request(response):
        request_latency = time.time() - flask.g.start_time
        http_request_latency_ms.labels(request.method, request.path).observe(request_latency)

        http_concurrent_request_count.dec()

        http_request_count.labels(request.method, request.path, response.status_code).inc()
        http_response_size_bytes.labels(request.method, request.path).observe(response.calculate_content_length())
        return response

    monitor_host_metrics()

    http_request_latency_ms = Histogram('http_request_latency_ms', 'HTTP Request Latency',
                                        ['method', 'endpoint'])

    http_request_size_bytes = Histogram('http_request_size_bytes', 'HTTP request size in bytes',
                                        ['method', 'endpoint'])

    http_response_size_bytes = Histogram('http_response_size_bytes', 'HTTP response size in bytes',
                                         ['method', 'endpoint'])

    http_request_count = Counter('http_request_count', 'HTTP Request Count', ['method', 'endpoint', 'http_status'])
    http_concurrent_request_count = Gauge('http_concurrent_request_count', 'Flask Concurrent Request Count')
    app.before_request(before_request)
    app.after_request(after_request)

    app.add_url_rule('/metrics', 'prometheus_metrics', view_func=metrics)


def metrics():
    registry = core.REGISTRY
    params = parse_qs(urlparse(request.path).query)
    if 'name[]' in params:
        registry = registry.restricted_registry(params['name[]'])
    output = generate_latest(registry)
    response = make_response(output)
    response.headers['Content-Type'] = CONTENT_TYPE_LATEST
    return response
