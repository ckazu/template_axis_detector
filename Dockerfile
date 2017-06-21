# ToDo: replace to alpine and reduce image size
FROM jjanzic/docker-python3-opencv
LABEL maintainer "ckazu.s@gmail.com"

COPY main.py /tmp
WORKDIR /tmp
ENTRYPOINT ["python3", "main.py"]
CMD ["--help"]
