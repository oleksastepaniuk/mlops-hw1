import grpc
from concurrent import futures
import time

# import the generated classes
from protobufs import question_pb2
from protobufs import question_pb2_grpc

# import the original question_service.py
from question.questions_service import QuestionsService as question

# create a class to define the server functions
# derived from question_pb2_grpc.QuestionControllerServicer
class QuestionControllerServicer(question_pb2_grpc.QuestionControllerServicer):

    # question.square_root is exposed here
    # the request and response are of the data types
    # generated as question_pb2.*

    def CreateOrUpdateQuestion(self, request, context):
        response = question_pb2.Question()
        response.id = question.create_or_update_question(request)
        return response

    def GetQuestions(self, request, context):
        response = question_pb2.Question()
        response.id = question.get_questions(request.question_id)
        return response
    
    def GetQuestion(self, request, context):
        print(request)
        response = question_pb2.Question()
        response.id = request.question_id
        # map request to service params
        # response.id = question.get_question(request.question_id).id
        return response
    
    def UpvoteQuestion(self, request, context):
        response = question_pb2.Question()
        response.id = question.upvote_question(request).id
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_QuestionServicer_to_server`
# to add the defined class to the created server
question_pb2_grpc.add_QuestionControllerServicer_to_server(
        QuestionControllerServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)