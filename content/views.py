# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Chapter, sql_to_json, save_json_to_db, build_db_from_files, save_db_to_files
from push_to_git import git_commit, git_clone, git_push, git_add
import json
import pickle
from shutil import rmtree

def index(request):
  try:
    rmtree('content/keidelclemens.github.io')
  except:
    pass
  git_clone('git@github.com:keidelclemens/keidelclemens.github.io.git', 'keidelclemens.github.io', 'content/')
  build_db_from_files()
  return render(request, 'index.html')

def save_data(request):
  try:
    rmtree('content/keidelclemens.github.io')
  except:
    pass
  git_clone('git@github.com:keidelclemens/keidelclemens.github.io.git', 'keidelclemens.github.io', 'content/')
  save_json_to_db(json.loads(request.POST.get('data')))
  save_db_to_files()
  git_add('.', 'content/keidelclemens.github.io/')
  git_commit('update content', 'content/keidelclemens.github.io/')
  git_push('content/keidelclemens.github.io')
  return render(request, 'index.html')

def retrieve_data(request):
  return HttpResponse(json.dumps(sql_to_json()), content_type="application/json")
