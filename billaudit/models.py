# billaudit/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    infra_image = models.ImageField(upload_to='hospital_infra/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    bill_image = models.ImageField(upload_to='bills/')
    extracted_text = models.TextField(blank=True)   # raw OCR output
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    analysis_result = models.TextField(blank=True)  # flagged discrepancies, notes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill #{self.id} - {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='reviews')

    overall_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    staff_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    treatment_name = models.CharField(max_length=150, blank=True)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    comment = models.TextField(blank=True)
    photo = models.ImageField(upload_to='review_photos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.overall_rating}★ by {self.user.username}"