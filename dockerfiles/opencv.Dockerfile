FROM borda/docker_python-opencv-ffmpeg:cpu-py3.10-cv4.6.0

WORKDIR /src

RUN pip install --upgrade pip
COPY ./requirements.txt /src/
RUN pip install -r requirements.txt

COPY . /src

CMD ["python", "src/process_stream.py"]