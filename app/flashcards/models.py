from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from enum import Enum

class ReviewStatus(str, Enum):
    FORGOT = 'forgot'
    HARD = 'hard'
    EASY = 'easy'

class FlashCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    front = models.TextField()
    back = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards')

    # Front review fields
    front_last_review = models.DateTimeField(null=True, blank=True)
    front_interval = models.IntegerField(default=1)  # in minutes
    front_review_count = models.IntegerField(default=0)
    front_easiness_factor = models.FloatField(default=2.5)
    front_repetitions = models.IntegerField(default=0)

    # Back review fields
    back_last_review = models.DateTimeField(null=True, blank=True)
    back_interval = models.IntegerField(default=1)  # in minutes
    back_review_count = models.IntegerField(default=0)
    back_easiness_factor = models.FloatField(default=2.5)
    back_repetitions = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"FlashCard {self.id}: {self.front[:30]}..."

    def is_due_for_review(self, side=None):
        """Check if the card is due for review. If side is specified, checks only that side.
        Otherwise checks both sides and returns True if either side is due."""
        if side:
            last_review = getattr(self, f'{side}_last_review')
            interval = getattr(self, f'{side}_interval')
            if not last_review:
                return True
            return last_review + timezone.timedelta(minutes=interval) <= timezone.now()
        else:
            # Check both sides
            return self.is_due_for_review('front') or self.is_due_for_review('back')

    def update_review(self, status: ReviewStatus, side='front'):
        """Update review status and schedule next review using SM-2 algorithm"""
        now = timezone.now()
        
        # Get current values
        ef = getattr(self, f'{side}_easiness_factor')
        reps = getattr(self, f'{side}_repetitions')
        interval = getattr(self, f'{side}_interval')
        review_count = getattr(self, f'{side}_review_count')

        # Update review count
        setattr(self, f'{side}_review_count', review_count + 1)
        setattr(self, f'{side}_last_review', now)

        # Apply SM-2 algorithm
        if status == ReviewStatus.FORGOT:
            reps = 0
            interval = 1
            ef = max(1.3, ef - 0.3)
        else:
            reps += 1
            if status == ReviewStatus.HARD:
                ef = max(1.3, ef - 0.15)
            elif status == ReviewStatus.EASY:
                ef = min(2.5, ef + 0.15)

            if reps == 1:
                interval = 1
            elif reps == 2:
                interval = 6
            else:
                interval = round(interval * ef)

        # Update values
        setattr(self, f'{side}_easiness_factor', ef)
        setattr(self, f'{side}_repetitions', reps)
        setattr(self, f'{side}_interval', interval)
        
        self.save()
