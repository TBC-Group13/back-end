from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
    )
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    accepted_count = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def update_like_count(self):
        """
        Update the total number of likes received across all answers.
        Call this method whenever likes/dislikes change.
        """
        self.like_count = self.answers.aggregate(
            total_likes=models.Count('likes')
        )['total_likes'] or 0
        self.save()

    def update_dislike_count(self):
        """
        Update the total number of dislikes received across all answers.
        Call this method whenever likes/dislikes change.
        """
        self.dislike_count = self.answers.aggregate(
            total_dislikes=models.Count('dislikes')
        )['total_dislikes'] or 0
        self.save()

    def update_accepted_count(self):
        """
        Update the total number of accepted answers.
        Call this method whenever an answer's is_correct status changes.
        """
        self.accepted_count = self.answers.filter(is_correct=True).count()
        self.save()

