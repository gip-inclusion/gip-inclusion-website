python manage.py migrate && cd otelcol-contrib && ./otelcol-contrib --config ./config.yaml &> otelcol-output.log & echo "$!" > otel-pid
