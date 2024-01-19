import grpc
import uuid

# import the generated classes
from protobufs import question_pb2
from protobufs import question_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = question_pb2_grpc.QuestionControllerStub(channel)

# create a valid request message
question_request = question_pb2.QuestionRequest(question_id='f2d57ecf-5d4c-4a09-9cc3-64482dae9998')

# make the call
response = stub.GetQuestion(question_request)

# et voilà
print(response.id)