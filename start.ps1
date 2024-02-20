docker build --tag theta_corrector:latest .
docker run --rm -v "${PWD}/photos:/opt/photo_tools/photos"  -it theta_corrector:latest