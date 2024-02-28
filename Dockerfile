FROM python:3.12-slim
# FROM continuumio/miniconda3

WORKDIR /usr/src/app

COPY . .

# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip uninstall -y pip
# RUN conda env create -f environment.yml
# RUN echo "source activate StarRailSim" > ~/.bashrc
# ENV PATH /opt/conda/envs/StarRailSim/bin:$PATH

WORKDIR /usr/src/app/starrailturnsim

EXPOSE 8050

CMD ["python", "./app.py"]