# Billing-System
## Intro
Hi Guys 👋

This is my first GUI project using Python tkinter, which displays a Menu of a hotel/cafe, takes order from customer and generates bill.
The menu is present in text files in the 'Menu' folder, and bills will be saved in text/pdf format in the 'Bill Records' folder.

## Concept Used
- Modules
``` py
import tkinter 
import os
import time
import re
import reportlab
```
- File Handling

## Parts Of Project
- Header: For the name of the cafe/hotel
- Customer Frame: User enters customer details(Name & Contact).
- Menu Frame: Menu displayed and some button associated to categorize menu also a button to update price.
- Item Frame: Selected item will be displayed in the item frame from where the user can add item, remove item, update quantity and clear fields.
- Order Frame: Changes and selections will be displayed in the Order list in the order frame.
- Billing Frame: User can generate bill after selecting at least 1 item also Order cancellation is provided.
- New Window: Bill will be displayed in a new window to the user and will be saved in the 'Bill Records' folder.
- Storage: Python Dictionary is used to store(Temporary Storage) customers' orders, and files (text & pdf) are used to store(Permanent Storage) menu and bills with customers information. 

## Issues
In case you have any difficulties or issues while trying to run the code, you can raise them on the issues.

## Pull Requests
If you have something to contribute, we welcome Pull Requests to improve the main project. I'll send your helpful contribution as soon as possible.

## Give it a Star ✴
If you find this repo useful, give it a Star

**I hope this will help you. Thank you**
