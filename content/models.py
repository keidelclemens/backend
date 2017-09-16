# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from os import listdir, unlink
from os.path import isfile, join
import os, shutil

class Book(models.Model):
  title = models.CharField(max_length=100)
  url = models.CharField(max_length=100)
  owner = models.CharField(max_length=20)
  content = models.CharField(max_length=1000)
  redirect_url = models.CharField(max_length=100)
  order = models.IntegerField()
  comments = models.BooleanField()

  def as_dictionary(self):
    book_dict = {}
    book_dict['title'] = self.title
    book_dict['content'] = self.content
    book_dict['url'] = self.url
    book_dict['redirect_url'] = self.redirect_url
    book_dict['comments'] = self.comments
    book_dict['chapters'] = []
    for chapter in Chapter.objects.order_by('order').filter(book = self):
        book_dict['chapters'].append(chapter.as_dictionary())
    return book_dict
  
  def __str__(self):
    return self.title

class Chapter(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  content = models.CharField(max_length=1000)
  title = models.CharField(max_length=100)
  url = models.CharField(max_length=100)
  order = models.IntegerField()
  heading = models.CharField(max_length=1000)
  
  def as_dictionary(self):
    chapter_dict = {}
    chapter_dict['title'] = self.title
    chapter_dict['content'] = self.content
    chapter_dict['url'] = self.url
    chapter_dict['heading'] = self.heading
    return chapter_dict
  
  def __str__(self):
    return str(self.book) + ' - ' + self.title

def build_db_from_files():
  Chapter.objects.all().delete()
  Book.objects.all().delete()
  book_filenames = [f for f in listdir('content/keidelclemens.github.io/_books/')]
  for book in book_filenames:
    save_book_from_file(book)
  chapter_filenames = [os.path.join(dp, f).replace('content/keidelclemens.github.io/_chapters/','') for dp, dn, filenames in os.walk('content/keidelclemens.github.io/_chapters/') for f in filenames]
  for chapter in chapter_filenames:
    save_chapter_from_file(chapter)

def save_book_from_file(fname):
  url = fname.split('.')[0]
  fname = 'content/keidelclemens.github.io/_books/' + fname
  f = open(fname, 'r')
  text = f.read()
  f.close()
  frontmatter = text.split('---\n')[1].split('\n')
  content = youtubeUnembed(text.split('---\n', 2)[-1])
  title = get_frontmatter_piece(frontmatter, 'title')
  owner = get_frontmatter_piece(frontmatter, 'owner')
  redirect_url = get_frontmatter_piece(frontmatter, 'redirect', '')
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
  url = fname.split('.')[0].split('/')[-1]
  fname = 'content/keidelclemens.github.io/_chapters/' + fname
  f = open(fname, 'r')
  text = f.read()
  f.close()
  frontmatter = text.split('---\n')[1].split('\n')
  content = youtubeUnembed(text.split('---\n', 2)[-1])
  title = get_frontmatter_piece(frontmatter, 'title')
  order = int(get_frontmatter_piece(frontmatter, 'order'))
  book_txt = get_frontmatter_piece(frontmatter, 'book')
  header = get_frontmatter_piece(frontmatter, 'header', '')
  book = Book.objects.filter(url=book_txt)[0]
  chapter = Chapter(book=book,
                    url=url,
                    content=content,
                    title=title,
                    heading=header,
                    order=order)
  chapter.save()

def get_frontmatter_piece(frontmatter, piece, default = None):
  for f in frontmatter:
    if f[:len(piece) + 2] == piece + ': ':
      return f[len(piece) + 2:]
  return default

def sql_to_json():
  all_data = {}
  all_data['ruth'] = []
  all_data['jonathan'] = []
  all_data['family'] = []

  books = Book.objects.order_by('order').all()
  for book in books:
    all_data[book.owner].append(book.as_dictionary())
  return all_data

def save_json_to_db(data):
  Chapter.objects.all().delete()
  Book.objects.all().delete()
  for owner in ['ruth', 'jonathan', 'family']:
    book_order_count = 1
    for book_obj in data[owner]:
      book = Book()
      book.title = book_obj['title']
      book.url = book_obj['url']
      book.owner = owner
      book.content = book_obj['content']
      try:
        book.redirect_url = book_obj['redirect_url']
      except:
        pass
      book.order = book_order_count
      book_order_count += 1
      try:
        book.comments = (book_obj['redirect_url'] == '')
      except:
        book.comments = True
      book.save()
      chapter_order_count = 1
      for chapter_obj in book_obj['chapters']:
        chapter = Chapter()
        chapter.book = book
        chapter.content = chapter_obj['content']
        chapter.title = chapter_obj['title']
        chapter.url = chapter_obj['url']
        chapter.order = chapter_order_count
        chapter_order_count += 1
        chapter.heading = ''
        if 'heading' in chapter_obj.keys():
          if len(chapter_obj['heading']) > 0:
            chapter.heading = chapter_obj['heading']
        chapter.save()

def save_db_to_files():
  books = Book.objects.all()
  book_folder = 'content/keidelclemens.github.io/_books/'
  chapter_folder = 'content/keidelclemens.github.io/_chapters/'
  # clear folders
  for folder in [book_folder, chapter_folder]:
    shutil.rmtree(folder)
    os.makedirs(folder)
  # build book files
  books = Book.objects.all()
  for book in books:
    filename = book_folder + book.url + '.html'
    f = open(filename, 'w')
    f.write('---\n')
    f.write('title: ' + book.title + '\n')
    f.write('order: ' + str(book.order) + '\n')
    f.write('layout: book\n')
    f.write('owner: ' + book.owner + '\n')
    if book.redirect_url != '': f.write('redirect: ' + book.redirect_url + '\n')
    f.write('---\n')
    f.write(youtubeEmbed(book.content))
    f.close()
  # build chapter files
  chapters = Chapter.objects.all()
  for chapter in chapters:
    filename = chapter_folder + chapter.book.url + '/' + chapter.url + '.html'
    if not os.path.exists(os.path.dirname(filename)):
      try:
        os.makedirs(os.path.dirname(filename))
      except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
          raise
    f = open(filename, 'w')
    f.write('---\n')
    f.write('title: ' + chapter.title + '\n')
    f.write('order: ' + str(chapter.order) + '\n')
    f.write('layout: chapter\n')
    f.write('book: ' + chapter.book.url + '\n')
    if len(chapter.heading) > 0:
      f.write('header: ' + chapter.heading + '\n')
    f.write('---\n')
    f.write(youtubeEmbed(chapter.content))
    f.close()

def youtubeEmbed(html):
  html = html.replace('<oembed>https://www.youtube.com/watch?v=', '<div class="videoWrapper"><iframe width="560" height="315" src="https://www.youtube.com/embed/')
  html = html.replace('</oembed>', '?rel=0" frameborder="0" allowfullscreen></iframe></div>')
  return html

def youtubeUnembed(html):
  html = html.replace('<iframe width="560" height="315" src="https://www.youtube.com/embed/', '<oembed>https://www.youtube.com/watch?v=')
  html = html.replace('?rel=0" frameborder="0" allowfullscreen></iframe>', '</oembed>')
  return html
