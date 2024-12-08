from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def check_completion(self):
        """
        Check if the question has a correct answer and update completion status
        """
        has_correct_answer = self.answers.filter(is_correct=True).exists()
        if has_correct_answer and not self.completed:
            self.completed = True
            self.save()


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_answers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.username}"
