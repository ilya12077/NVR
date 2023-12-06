FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y emacs && apt-get install libgl1 &&\
    apt-get autoremove -y
	
# Install software 
RUN apt-get install -y git


# Clone the conf files into the docker container
RUN git clone https://github.com/ilya12077/NVR.git
	
	
RUN cp -a ./NVR/. /etc/nvr/
RUN rm -r -f ./NVR/

RUN pip install opencv-python requests Flask waitress

ENV AM_I_IN_A_DOCKER_CONTAINER Yes
EXPOSE 8881/tcp
CMD ["python", "/etc/nvr/main.py"]

