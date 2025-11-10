# run with uvicorn by default (without tls)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# run with uvicorn by default (with tls)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem

# create certificate to enable http2
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"

# run with http2
hypercorn app.main:app \
 --bind 127.0.0.1:8000 \
 --certfile cert.pem \
 --keyfile key.pem

# check run with http2
curl -v -k --http2 https://127.0.0.1:8000/api/v1/authors/
