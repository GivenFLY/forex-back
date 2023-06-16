from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from questions.serializers import QuestionSerializer, AnswerSerializer
from django.conf import settings


class AssistantAPIView(generics.GenericAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data.get("question")

        answer = settings.ASSISTANT.answer(question)

        return Response(
            AnswerSerializer({"answer": answer}).data, status=status.HTTP_200_OK
        )
