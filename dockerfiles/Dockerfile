FROM python:3.9-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC0
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsm6 libxext6 libxrender-dev libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

  RUN pip3 install --upgrade pip
  # Install required packages
  # For psycopg2 and Git
  
  # Install requirements
  RUN pip install --upgrade pip

  RUN pip install --upgrade pip setuptools wheel
  RUN pip install Django
  RUN pip install psycopg2-binary
  
  # RUN apt-get update && apt-get install -y \
  #   libsm6 \
  #   libxext6 \
  #   libxrender-dev

# Install OpenCV using pip
  RUN pip install opencv-python
  COPY ../requirements.txt /root/kinderneutron
  RUN pip install -r requirements.txt
  # Create directories  
  RUN mkdir -p /root/workspace/src
  RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
  COPY ./  /root/kinderneutron
  # Switch to project directory
  WORKDIR /root/kinderneutron
  EXPOSE 8000
  EXPOSE 8001
