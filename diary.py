#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import sys

from peewee import * 

# Create database
db = SqliteDatabase('diary.db') 

# database model creation
class Entry(Model):
  content = TextField()
  timestamp = DateTimeField(default=datetime.datetime.now)
  
  class Meta:
    database = db

# Connecting model to database
def initialize():
  """Create the database and the table if they don't exist."""
  db.connect()
  db.create_tables([Entry], safe=True)

# Clear program window after an action
def clear():
  os.system('cls' if os.name == 'nt' else 'clear')  

# Create menu for diary
def menu_loop():
  """show the menu"""
  choice = None
  
  while choice != 'q':
    clear()
    print("Enter 'q' to quit.")
    for key, value in menu.items():
      print('{}) {}'.format(key, value.__doc__)) 
    choice = input('Action: ').lower().strip()
    
    if choice in menu:     
      clear()
      menu[choice]()       #run method if input choice is in menu dictionary
  
  
# Add entry to diary from menu
def add_entry():
  """Add an entry"""
  print("Enter your entry. Press ctrl+d when finished.")
  data = sys.stdin.read().strip()
  
  if data:
    if input('\nSave entry? [y/n]').lower() != 'n':
             Entry.create(content=data)
             print("Saved successfully!")

# View entry selection from menu
def view_entries(search_query=None):
  """View previous entries"""
  entries = Entry.select().order_by(Entry.timestamp.desc())
  if search_query:
    entries = entries.where(Entry.content.contains(search_query))
  
  for entry in entries:
    timestamp = entry.timestamp.strftime(' %A %B %d, %Y %I:%M%p')
    clear()
    print(timestamp)
    print('='*len(timestamp))
    print(entry.content)
    print('\n\n'+'='*len(timestamp))
    print('n) next entry')
    print('d) delete entry')
    print('q) return to main menu')
    
    next_action = input('action: [n/d/q]').lower().strip()
    
    if next_action == 'q':
      break
    
    elif next_action == 'd':
      delete_entry(entry)

# Search entry with keyword from menu  
def search_entries():
  """Search entries for a word."""
  view_entries(input('Search query: '))

# Delete an entry from the diary  
def delete_entry(entry):
  """Delete an entry"""
  if input("Are you sure? [y/n]").lower() == 'y':
    entry.delete_instance()
    print("Entry deleted..")

# Ordered Dictionary containing menu options(which represents the funtions)
menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
  ])
  

if __name__ == '__main__':
  initialize()
  menu_loop()
