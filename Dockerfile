FROM python:3-alpine
ENV BOT_TOKEN=''
WORKDIR /app
COPY . /app
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt
CMD ["python3", "main.py"]



docker build -t said2007/image_name .

docker push username/image_name

docker run -e BOT_TOKEN="7021904114:AAEQv1cJtLFZtNrdjHEgCnZ9Zz6Qx10MU_w" said2007/exams_image