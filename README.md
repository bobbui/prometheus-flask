# prometheus-flask
Library to expose Prometheus performance metrics on Flask application

Metric will be exposed on the same port as main Flask application

## Available metrics
    - Host metrics:
         - Up time
         - CPU usage: percent, CPU time for user/system
         - Memory usage: total, available, cached, swap
         - IO usage: number of read/write operation
         - Networking: in and out: drop/packet/bytes/erros
    - Web application metrics:
         - Request Response time
         - Request size.
         - Response size.
         - Throughput
         - HTTP status breakdown

## Dashboard

Start Grafana, import the Grafana-dashboard.json, profit!

# Installation

Install dependencies

```
pip install -r requirements.txt
```

Run

```
python main.py
```



