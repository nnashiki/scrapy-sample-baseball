FROM jupyter/datascience-notebook

LABEL  maintainer "nashiki <n.nashiki.work@gmail.com>"

RUN curl -L  "https://oscdl.ipa.go.jp/IPAexfont/ipaexg00301.zip" > font.zip
RUN unzip font.zip
RUN cp ipaexg00301/ipaexg.ttf /opt/conda/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/ipaexg.ttf
RUN echo "font.family : IPAexGothic" >>  /opt/conda/lib/python3.6/site-packages/matplotlib/mpl-data/matplotlibrc
RUN rm -r ./.cache

RUN pip install -U pip
RUN pip install --upgrade setuptools
RUN pip install pymysql \
                pandas \
                matplotlib \
                ipython-sql \
                RISE

RUN jupyter-nbextension install rise --py --sys-prefix
RUN jupyter-nbextension enable rise --py --sys-prefix
