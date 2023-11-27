# Billing-System
## Intro
Hi Guys 👋

This is my first GUI project using python tkinter which display Menu of hotel/cafe, takes order from customer and generates bill.
Menu is present in text files in 'Menu' folder and bills will be saved in text/pdf format in 'Bill Records' folder.

## Concept Used
- Modules
```py
import tkinter 
import os
import time
import re
import reportlab
```
- File Handling

## Parts Of Project
- Header: For name of cafe/hotel
- Customer Frame: User enters customer details(Name & Contact).
- Menu Frame: Menu displayed and some button associated to categorize menu also a button to update price .
- Item Frame: Selected item will be displayed in item frame from where user can add item, remove item, update quantity and clear fields.
- Order Frame: Changes and selection will be displayed in Order list in order frame.
- Billing Frame: User can generate bill after selecting at least 1 item also Order cancellation is provided.
- New Window: Bill will be displayed in new window to user and will be saved in 'Bill Records' folder.
- Storage: Python Dictionary is used to store(Temporary Storage) customer's order and file(text & pdf) are used to store(Permanent Storage) menu and bills with customers information. 

## Issues
Incase you have any difficulties or issues while trying to run the code you can raise it on the issues

## Pull Requests
If you have something to contribute, we welcome Pull Requests to improve the main project, your helpful contribution will be distributed as soon as possible.

## Give it a Star ✴
If you find this repo useful , give it a Star

**I hope this will help you Thanku**