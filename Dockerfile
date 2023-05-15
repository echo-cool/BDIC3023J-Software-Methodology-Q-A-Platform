FROM python:3.9.7
COPY . /debugger
WORKDIR /debugger
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["flasky.py"]
