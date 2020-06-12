FROM continuumio/miniconda3:latest

ENV DEBIAN_FRONTEND noninteractive

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Pull the environment name out of the environment.yml
RUN echo "source activate s3DataViewerEnv" >> ~/.bashrc
ENV PATH /opt/conda/envs/s3DataViewerEnv/bin:$PATH
#ENV PATH /opt/conda/envs/sp_env/bin:$PATH



#RUN echo "conda activate s3ImageCloud" > ~/.bashrc
#ENV PATH /opt/conda/envs/sp_env/bin:$PATH
ENV PYTHONPATH /code:/code/backend
#ENV PYTHONUNBUFFERED 1
COPY . /code/backend
WORKDIR /code/backend
EXPOSE 8080

CMD ["python", "/code/backend/s3DataViewer"]