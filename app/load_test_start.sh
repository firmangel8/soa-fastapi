locust -f locustfile.py \
  --host http://127.0.0.1:8000 \
  --users 1000 \
  --spawn-rate 50 \
  --run-time 10m
