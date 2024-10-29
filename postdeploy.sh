python manage.py migrate
cd otecol-contrib && ./otelcol-contrib --config ./config.yaml &> otelcol-output.log & echo "$!" > otel-pid
