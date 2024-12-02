from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer, Tag
from .serializers import QuestionSerializer, CreateQuestionSerializer, AnswerSerializer, TagSerializer
from django.db.models import Q


class QuestionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            tags_data = request.data.get('tags', [])
            tags = []
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)

            question = serializer.save(author=request.user)
            question.tags.set(tags)
            question.save()
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            answer = serializer.save(author=request.user, question=question)
            return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeDislikeAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, answer_id, action):
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == "like":
            answer.likes.add(request.user)
            answer.dislikes.remove(request.user)
        elif action == "dislike":
            answer.dislikes.add(request.user)
            answer.likes.remove(request.user)
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Action performed"}, status=status.HTTP_200_OK)


class MarkCorrectAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, answer_id):
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found"}, status=status.HTTP_404_NOT_FOUND)

        if answer.question.author != request.user:
            return Response({"error": "Only the question author can mark an answer as correct"}, status=status.HTTP_403_FORBIDDEN)

        Answer.objects.filter(question=answer.question).update(is_correct=False)
        answer.is_correct = True
        answer.save()
        return Response({"success": "Answer marked as correct"}, status=status.HTTP_200_OK)


class TagListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        tag = request.GET.get('tag', None)

        questions = Question.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        if tag:
            questions = questions.filter(tags__name=tag)

        results = [
            {
                "id": question.id,
                "title": question.title,
                "description": question.description,
                "tags": [tag.name for tag in question.tags.all()]
            }
            for question in questions
        ]

        return Response(results, status=status.HTTP_200_OK)

