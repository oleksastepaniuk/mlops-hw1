
based on https://github.com/ramananbalakrishnan/basic-grpc-python
https://realpython.com/python-microservices-grpc/
```
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protobufs/question.proto
```
