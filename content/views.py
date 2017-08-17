# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Book, Chapter

def index(request):
  books = Book.objects.all()
  return render(request, 'index.html', {'books': books})
