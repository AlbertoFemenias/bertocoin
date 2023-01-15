FROM python:3.11
RUN pip3 install poetry==1.3.1
RUN apt-get update && apt-get install secure-delete
RUN mkdir /docker_app
WORKDIR /docker_app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
COPY pyproject.toml /docker_app
RUN poetry install --only main
ENTRYPOINT [ "poetry", "run", "python", "bertocoin"]

# docker build . -t bertocoin
# docker run --rm -v $(pwd):/docker_app bertocoin -s=1234 -n=3 -d=10 -t=60 --passphrase='D46M9vCkKHHhiFsHK1-MC2G8O9Y4UCemx2U9sFPljy/)rlg-nFT5IH64l3uldFXb'
