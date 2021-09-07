FROM python:3.7.7
WORKDIR /debugger
COPY . /debugger
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flasky.py"]