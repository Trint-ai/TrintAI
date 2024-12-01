FROM python:3.12.0

RUN apt-get -y update
RUN apt-get install -y build-essential python3.11-dev libhdf5-dev ffmpeg

ADD backend/requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt

ADD backend/ backend/
WORKDIR backend/app
CMD ["python","-u","main.py"]
EXPOSE 8000
