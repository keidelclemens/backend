# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Book, Chapter, sql_to_json, build_db_from_files

def index(request):
  books = Book.objects.all()
  all_data = sql_to_json()
  return render(request, 'index.html', {'all_data': str(all_data)})
