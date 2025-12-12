FROM python:3.7

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        gcc \
        g++ \
        libffi-dev \
        musl-dev

ENV PYTHONIOENCODING=utf-8
ENV MKL_NUM_THREADS=16
WORKDIR /app

RUN adduser --disabled-password --gecos "app" app && \
    chown -R app:app /app
USER app

ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app requirements.txt .
RUN pip install --user -r requirements.txt && \
    rm requirements.txt


RUN wget https://s3.hpc.ut.ee/estnltk/estnltk_resources/neural_morph_softmax_emb_cat_sum_2019-08-23.zip && \
    mkdir -p softmax_emb_cat_sum/output/ && \
    unzip neural_morph_softmax_emb_cat_sum_2019-08-23.zip && \
    mv neural_morph_disamb/softmax_emb_cat_sum_23-08-2019/output softmax_emb_cat_sum && \
    rm -r neural_morph_softmax_emb_cat_sum_2019-08-23.zip neural_morph_disamb

COPY --chown=app:app . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--proxy-headers"]