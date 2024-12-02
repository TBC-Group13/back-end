from django.urls import path
from .views import (
    QuestionListCreateAPIView, AnswerListCreateAPIView,
    LikeDislikeAnswerAPIView, MarkCorrectAnswerAPIView, TagListCreateAPIView, SearchAPIView,
)

urlpatterns = [
    path('questions/', QuestionListCreateAPIView.as_view(), name='question-list-create'),
    path('questions/<int:question_id>/answers/', AnswerListCreateAPIView.as_view(), name='answer-list-create'),
    path('answers/<int:answer_id>/mark-correct/', MarkCorrectAnswerAPIView.as_view(), name='mark-correct-answer'),
    path('answers/<int:answer_id>/<str:action>/', LikeDislikeAnswerAPIView.as_view(), name='like-dislike-answer'),
    path('tags/', TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('questions/search/', SearchAPIView.as_view(), name='search-questions'),
]
