docker buildx build --platform linux/amd64 -t semanticshield:0.1.1 .
docker images | grep shield