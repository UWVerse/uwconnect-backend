docker stop uwconnect-be
docker build --tag ece651-uwconnect-be --label ece651-uwconnect-be .
docker image prune --force --filter "label=ece651-uwconnect-be"
docker container prune --force --filter "label=uwconnect-be"
docker run -d -p 5000:5000 --name uwconnect-be --label uwconnect-be ece651-uwconnect-be