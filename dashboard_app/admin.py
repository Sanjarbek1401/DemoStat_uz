from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
# import pandas as pd
import os
import openpyxl
from django.http import JsonResponse

from .models import Region, StatisticsData, ExcelImport, PdfResource, RepublicStatistics

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'svg_id')
    search_fields = ('name', 'svg_id')

@admin.register(StatisticsData)
class StatisticsDataAdmin(admin.ModelAdmin):
    list_display = ('region', 'year', 'gender', 'age_min', 'age_max', 'population')
    list_filter = ('year', 'gender', 'region')
    search_fields = ('region__name',)
    actions = ['import_xlsx']
    
    def age_range(self, obj):
        if obj.age_max:
            return f"{obj.age_min}-{obj.age_max}"
        return f"{obj.age_min}+"
    
    age_range.short_description = "Age Range"

    def import_xlsx(self, request, queryset=None):
        if request.method == 'POST' and 'apply' in request.POST:
            xlsx_file = request.FILES['xlsx_file']
            wb = openpyxl.load_workbook(xlsx_file)
            ws = wb.active
            # Ustunlar: Age, Year, Genders (Male, Female), population
            for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                age, year, gender, population = row
                # Gender mapping
                gender_map = {
                    'Male': 'erkak', 'Female': 'ayol', 'Umumiy': 'jami',
                    'Erkak': 'erkak', 'Ayol': 'ayol', 'Jami': 'jami',
                    'male': 'erkak', 'female': 'ayol', 'umumiy': 'jami', 'jami': 'jami'
                }
                db_gender = gender_map.get(str(gender).strip(), 'jami')
                # Age parsing
                if isinstance(age, str) and '-' in age:
                    age_min, age_max = age.split('-')
                    age_min = int(age_min.strip())
                    age_max = int(age_max.strip())
                elif isinstance(age, (int, float)):
                    age_min = int(age)
                    age_max = int(age)
                else:
                    age_min = 0
                    age_max = 0
                # Regionni tanlash (admin panelda filtrdan yoki querysetdan olishingiz mumkin)
                # Bu yerda faqat birinchi tanlangan regionga import qilamiz (yoki kerakli logikani o'zgartiring)
                if queryset and queryset.exists():
                    region = queryset.first().region
                else:
                    self.message_user(request, f"Region aniqlanmadi (qator {i})", level=messages.ERROR)
                    continue
                obj, created = StatisticsData.objects.update_or_create(
                    region=region,
                    year=year,
                    gender=db_gender,
                    age_min=age_min,
                    age_max=age_max,
                    defaults={'population': population}
                )
            self.message_user(request, "XLSX fayldan ma'lumotlar import qilindi!", level=messages.SUCCESS)
            return redirect(request.get_full_path())
        form = XLSXImportForm()
        return render(request, 'admin/xlsx_import.html', {'form': form})

    import_xlsx.short_description = "XLSX fayldan import qilish (tanlangan region uchun)"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-xlsx/', self.admin_site.admin_view(self.import_xlsx), name='statisticsdata_import_xlsx'),
        ]
        return custom_urls + urls

class ExcelImportForm(forms.ModelForm):
    class Meta:
        model = ExcelImport
        fields = ('file',)

# @admin.register(ExcelImport)
# class ExcelImportAdmin(admin.ModelAdmin):
#     list_display = ('uploaded_at', 'processed', 'records_imported')
#     form = ExcelImportForm
#     change_list_template = 'admin/excel_import_change_list.html'
    
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('import-excel/', self.import_excel, name='import_excel'),
#         ]
#         return custom_urls + urls
    
#     def import_excel(self, request):
#         if request.method == "POST":
#             form = ExcelImportForm(request.POST, request.FILES)
#             if form.is_valid():
#                 excel_import = form.save()
#                 try:
#                     # Process the Excel file
#                     df = pd.read_excel(excel_import.file.path)
#                     records_imported = self.process_excel_data(df)
                    
#                     # Update import record
#                     excel_import.processed = True
#                     excel_import.records_imported = records_imported
#                     excel_import.save()
                    
#                     messages.success(request, f"Successfully imported {records_imported} records from Excel file.")
#                 except Exception as e:
#                     messages.error(request, f"Error processing Excel file: {str(e)}")
                
#                 return redirect('..')
#         else:
#             form = ExcelImportForm()
        
#         return render(
#             request,
#             'admin/excel_import_form.html',
#             {
#                 'form': form,
#                 'opts': self.model._meta,
#             }
#         )
    
#     def process_excel_data(self, df):
#         # Expected columns: year, region, age_min, age_max, gender, population
#         records_imported = 0
        
#         for _, row in df.iterrows():
#             # Get or create region
#             region_name = row['region']
#             region, _ = Region.objects.get_or_create(
#                 name=region_name,
#                 defaults={'svg_id': region_name.lower().replace(' ', '_')}
#             )
            
#             # Process age range
#             age_min = row['age_min']
#             age_max = row['age_max'] if 'age_max' in row and not pd.isna(row['age_max']) else None
            
#             # Create or update statistics data
#             stats, created = StatisticsData.objects.update_or_create(
#                 region=region,
#                 year=row['year'],
#                 age_min=age_min,
#                 age_max=age_max,
#                 gender=row['gender'].lower(),
#                 defaults={
#                     'population': int(row['population'])
#                 }
#             )
            
#             if created:
#                 records_imported += 1
        
#         return records_imported

@admin.register(PdfResource)
class PdfResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(RepublicStatistics)
class RepublicStatisticsAdmin(admin.ModelAdmin):
    list_display = ('year', 'total_population', 'age_min', 'age_max', 'age_population')
    list_filter = ('year',)

def republic_stats_api(request):
    year = int(request.GET.get('year', 2026))
    age_min = int(request.GET.get('min_age', 0))
    age_max = int(request.GET.get('max_age', 85))
    try:
        stats = RepublicStatistics.objects.get(year=year, age_min=age_min, age_max=age_max)
        data = {
            'total_population': stats.total_population,
            'age_range': f'{age_min}-{age_max}',
            'age_population': stats.age_population,
        }
    except RepublicStatistics.DoesNotExist:
        data = {
            'total_population': 0,
            'age_range': f'{age_min}-{age_max}',
            'age_population': 0,
        }
    return JsonResponse(data)
