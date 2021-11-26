FROM python:3.9.7
COPY . /debugger
WORKDIR /debugger
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5000
CMD ["flasky.py"]