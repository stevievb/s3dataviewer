FROM continuumio/miniconda3:latest AS install


ENV DEBIAN_FRONTEND noninteractive

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml



# Pull the environment name out of the environment.yml
RUN echo "source activate s3DataViewerPlotServerEnv" >> ~/.bashrc
ENV PATH /opt/conda/envs/s3DataViewerPlotServerEnv/bin:$PATH


ENV PYTHONPATH /code:/code/backend
#ENV PYTHONUNBUFFERED 1
COPY . /code/backend
WORKDIR /code/backend

RUN conda clean -ay

EXPOSE 5006

RUN python3 -c "import tornado; print('tornado version=' + tornado.version)"
RUN bokeh info


CMD ["python", "/code/backend/s3DataViewerPlotServer"]