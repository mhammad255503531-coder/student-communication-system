# Student Communication System

## Overview

This project is a simple **Student Communication System** built in Python. It allows users to send messages and emails, manage accounts, and track activity through a role-based system.

The system supports two types of users:

* **Students**
* **Auditors (Admin role)**

---

## Features

### Student Features

* Login and logout system
* Send private messages
* Send public messages
* View received messages
* Send emails
* View received emails

### Auditor Features

* View all messages
* View all emails
* Search messages by user
* Search emails by user
* Filter messages by date and time
* Count messages sent and received by a user
* View login history
* Manage users (edit password, role, delete user)

---

## Technologies Used

* Python
* JSON (for data storage)
* File handling

---

## Project Structure

* `Finalproject2025.py` → Main application file
* `users.txt` → Stores user data
* `messages.txt` → Stores messages
* `emails.txt` → Stores emails
* `history.txt` → Stores login history

---

## How It Works

1. The system initializes default users if files do not exist
2. User logs in with username and password
3. Based on role, user gets access to specific features
4. All actions are stored in files for tracking

---

## Default Login Credentials

```
Username: student1
Password: 123

Username: student2
Password: 123

Username: admin
Password: 123
```

---

## Notes

* Messages and emails have character limits
* Data is stored locally in text files
* The system runs in the terminal

---

## Author

Muhammad Hammad Iftikhar
