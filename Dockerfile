FROM python:3.12-slim

WORKDIR /usr/src/app

COPY . .

# RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
# RUN python -m pip uninstall -y pip

ENV CONTAINER=True

WORKDIR /usr/src/app/starrailturnsim
    
EXPOSE 8050

CMD ["python", "./app.py"]