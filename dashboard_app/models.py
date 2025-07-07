from django.db import models
from django.core.validators import FileExtensionValidator

class Region(models.Model):
    """Model for Uzbekistan regions"""
    name = models.CharField(max_length=100)
    svg_id = models.CharField(max_length=100, help_text='ID of the region in SVG map')
    
    def __str__(self):
        return self.name

class StatisticsData(models.Model):
    """Model for storing demographic statistics data"""
    GENDER_CHOICES = [
        ('jami', 'Jami'),
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol'),
    ]
    
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='statistics')
    year = models.IntegerField()
    age_min = models.IntegerField()
    age_max = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    population = models.IntegerField()
    
    class Meta:
        verbose_name = 'Statistics Data'
        verbose_name_plural = 'Statistics Data'
        indexes = [
            models.Index(fields=['region', 'year']),
            models.Index(fields=['age_min', 'age_max']),
            models.Index(fields=['gender']),
        ]
    
    def __str__(self):
        age_range = f"{self.age_min}-{self.age_max if self.age_max else '+'}"
        return f"{self.region.name} - {self.year} - {age_range} - {self.gender} - {self.population}"

class ExcelImport(models.Model):
    """Model to track Excel data imports"""
    file = models.FileField(
        upload_to='excel_imports/',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    records_imported = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Import on {self.uploaded_at.strftime('%Y-%m-%d %H:%M')} - {self.records_imported} records"

class PdfResource(models.Model):
    title = models.CharField("Nomi", max_length=255)
    description = models.TextField("Qisqacha ma'lumot", blank=True)
    pdf_file = models.FileField("PDF fayl", upload_to='resources_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RepublicStatistics(models.Model):
    year = models.PositiveIntegerField()
    total_population = models.BigIntegerField()
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()
    age_population = models.BigIntegerField()
    # Qo'shimcha statistikalar ham qo'shish mumkin

    class Meta:
        unique_together = ('year', 'age_min', 'age_max')
