from django.urls import path
from .views import (
    QuestionListCreateAPIView, AnswerListCreateAPIView,
    LikeDislikeAnswerAPIView, MarkCorrectAnswerAPIView, TagListCreateAPIView, SearchAPIView, QuestionAnswersListView,
    UserQuestionListAPIView,
)

urlpatterns = [
    path('questions/', QuestionListCreateAPIView.as_view(), name='question-list-create'),
    path('questions/<int:question_id>/answers/', AnswerListCreateAPIView.as_view(), name='answer-list-create'),
    path('answers/<int:answer_id>/mark-correct/', MarkCorrectAnswerAPIView.as_view(), name='mark-correct-answer'),
    path('answers/<int:answer_id>/<str:action>/', LikeDislikeAnswerAPIView.as_view(), name='like-dislike-answer'),
    path('tags/', TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('questions/search/', SearchAPIView.as_view(), name='search-questions'),
    path('questions/<int:question_id>/list-answers/', QuestionAnswersListView.as_view(), name='question-answers'),
    path('personal/questions/', UserQuestionListAPIView.as_view(), name='user-questions'),
]

"""
curl -X GET http://127.0.0.1:8000/api/personal/questions/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNTc2NDk1LCJpYXQiOjE3MzM1NzI4OTUsImp0aSI6ImNmNTg4YmNkZGFkMTQ4MzZiNmRhNjU1ZmQ2Mjg5MDA4IiwidXNlcl9pZCI6MX0.fED_pREN9kesMiXXPIXe5kQFKUjKB9UrAuaJHlb3uyc"
"""