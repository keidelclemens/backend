# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from os import listdir
from os.path import isfile, join

class Book(models.Model):
  title = models.CharField(max_length=100)
  url = models.CharField(max_length=100)
  owner = models.CharField(max_length=20)
  content = models.CharField(max_length=1000)
  redirect_url = models.CharField(max_length=100)
  order = models.IntegerField()
  comments = models.BooleanField()

class Chapter(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  content = models.CharField(max_length=1000)
  title = models.CharField(max_length=100)
  url = models.CharField(max_length=100)

def build_db_from_files():
  book_filenames = [f for f in listdir('keidelclemens.github.io/_books/')]
  for book in book_filenames:
    save_book_from_file(book)
  chapter_filenames = [f for f in listdir('keidelclemens.github.io/_chapters/')]
  for chapter in chapter_filenames:
    save_book_from_file(chapter)

def save_book_from_file(fname):
  url = fname.split('.')[0]
  fname = 'keidelclemens.github.io/_books/' + fname
  f = open(fname, 'r')
  text = f.read()
  f.close()
  frontmatter = text.split('---\n')[1].split('\n')
  content = text.split('---\n', 2)[-1]
  title = get_frontmatter_piece(frontmatter, 'title')
  owner = get_frontmatter_piece(frontmatter, 'owner')
  redirect_url = get_frontmatter_piece(frontmatter, 'redirect')
  comments_txt = get_frontmatter_piece(frontmatter, 'comments')
  if comments_txt == 'false': comments = False
  else: comments = True
  order = int(get_frontmatter_piece(frontmatter, 'order'))
  book = Book(title=title,
              url=url,
              owner=owner,
              content=content,
              redirect_url=redirect_url,
              order=order,
              comments=comments)
  book.save()

def save_chapter_from_file(fname):
  url = fname.split('.')[0]
  fname = 'keidelclemens.github.io/_chapters/' + fname
  f = open(fname, 'r')
  text = f.read()
  f.close()
  frontmatter = text.split('---\n')[1].split('\n')
  content = text.split('---\n', 2)[-1]
  title = get_frontmatter_piece(frontmatter, 'title')
  order = int(get_frontmatter_piece(frontmatter, 'order'))
  book_txt = get_frontmatter_piece(frontmatter, 'book')
  book = Book.objects.filter(url=book_txt)
  chapter = Chapter(book=book,
                    url=url,
                    content=content,
                    title=title)
  chapter.save()


def get_frontmatter_piece(frontmatter, piece):
  for f in frontmatter:
    if f[:len(piece) + 2] == piece + ': ':
      return f[len(piece) + 2:]
  return None
