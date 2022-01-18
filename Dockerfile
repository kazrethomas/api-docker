FROM python:3.8

ADD final.py /
ADD new.db /

ADD requirements.txt /

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "final.py" ]



