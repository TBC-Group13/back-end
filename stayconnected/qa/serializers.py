from rest_framework import serializers
from .models import Question, Answer, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ['id', 'text', 'author', 'is_correct', 'likes', 'dislikes', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = TagSerializer(many=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'author', 'tags', 'answers', 'created_at', 'updated_at']


class CreateQuestionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']
