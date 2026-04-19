import json
import os
from datetime  import datetime
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
user_file = "users.txt"
messages_file = "messages.txt"
emails_file = "emails.txt"
history_file = "history.txt"
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def load_json(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []
def log_history(username, action):
    record = {
        "username": username,
        "action": action,
        "timestamp": now()
    }
    try:
        history = load_json(history_file) or []
        history.append(record)
        with open(history_file, 'w') as h:
            json.dump(history, h, indent=2)
    except Exception as e:
        print(f"Error logging: {e}")
def init_system():
    if os.path.exists(user_file) and os.path.exists(messages_file) and os.path.exists(emails_file) and os.path.exists(history_file):
        return
    users = [
        {"username": "student1", "password": "123", "role": "student"},
        {"username": "student2", "password": "123", "role": "student"},
        {"username": "admin", "password": "123", "role": "auditor"}    
    ]
    with open(user_file, 'w') as f:
        json.dump(users, f, indent=2)
    for filename in [messages_file, emails_file, history_file]:
        with open(filename, 'w') as f:
            json.dump([], f)
def save_users(users):
    with open(user_file, 'w') as f:
        json.dump(users, f, indent=2)
    print("Users saved successfully.")
def admin_manage_users():
    print("User Management")
    users = load_json(user_file)
    if not users:
        print("No users found")
        return
    print("All Users:")
    for idx, user in enumerate(users, 1):
        print(f"{idx}. Username: {user['username']}, Role: {user['role']}")
    choice = input("Enter user number to edit or 0 to go back: ")
    if choice == '0':
        return
    try:
        user_idx = int(choice) - 1
        if 0 <= user_idx < len(users):
            selected_user = users[user_idx]
            print(f"Editing user: {selected_user['username']}")
            print("1. Change Password")
            print("2. Change Role")
            print("3. Delete User")
            edit_choice = input("Enter choice: ")
            if edit_choice == '1':
                new_pass = input("Enter new password: ")
                selected_user['password'] = new_pass
                save_users(users)
                print("Password updated.")
            elif edit_choice == '2':
                print("1. Student2. Auditor")
                role_choice = input("Select new role: ")
                selected_user['role'] = 'student' if role_choice == '1' else 'auditor'
                save_users(users)
                print("Role updated.")
            elif edit_choice == '3':
                users.pop(user_idx)
                save_users(users)
                print("User deleted.")
    except ValueError:
        print("Invalid selection.")
def login():
    print("Welcome to the student book login system")
    user_input = input("Username= ")
    pass_input = input("Password= ")
    users = load_json(user_file)
    if not users:
        print("Error: Could not load users database.")
        return None
    for user in users:
        if user['username'] == user_input and user['password'] == pass_input:
            print(f"Login Successful as {user['role']}!")
            log_history(user_input, "LOGIN")
            return user
    print("Error! Invalid username or password.")
    return None
def logout(username):
    log_history(username, "LOGOUT")
    print(f"User {username} logged out successfully.")
def send_private(username):
    print("Send Private Message")
    recipient = input("Enter recipient username: ")
    content = input("Enter message: ")
    if not content:
        print("Message cannot be empty.")
        return
    if len(content) > 30:
        print("Message cannot be more than 30 characters.")
        return
    messages = load_json(messages_file) or []
    message = {
        "sender": username,
        "recipient": recipient,
        "content": content,
        "type": "private",
        "timestamp": now()
    }
    messages.append(message)
    try:
        with open(messages_file, 'w') as f:
            json.dump(messages, f, indent=2)
        print("Private message sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
def send_public(username):
    print("Send Public Message ")
    content = input("Enter message: ")
    if not content:
        print("Message cannot be empty.")
        return
    if len(content) > 30:
        print("Message cannot be more than 30 characters.")
        return
    messages = load_json(messages_file) or []
    message = {
        "sender": username,
        "recipient": "PUBLIC",
        "content": content,
        "type": "public",
        "timestamp": now()
    }
    messages.append(message)
    try:
        with open(messages_file, 'w') as f:
            json.dump(messages, f, indent=2)
        print("Public message sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
def view_messages(username):
    print(f"Your Messages")
    messages = load_json(messages_file)
    if not messages:
        print("No messages found.")
        return
    found = False
    for msg in messages:
        if (msg.get('type') == 'private' and msg.get('recipient') == username) or msg.get('type') == 'public':
            print(f"[{msg.get('timestamp')}] From: {msg.get('sender')} (Type: {msg.get('type', 'unknown').upper()})")
            print(f"Message: {msg.get('content', '')}")
            found = True
    if not found:
        print("No messages for you.")
def student_menu(username):
    while True:
        print(f" Student menu for ({username})")
        print("1. View Messages  2.Send Private Message   3. Send Public Message    4.View Emails   5.Send Email   6.Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            view_messages(username)
        elif choice == '2':
            send_private(username)
        elif choice == '3':
            send_public(username)
        elif choice == '4':
            view_emails(username)
        elif choice == '5':
            send_email(username)
        elif choice == '6':
            log_history(username, "LOGOUT")
            break
        else:
            print("Invalid choice.")
def send_email(username):
    print("Send Email ")
    recipient = input("Enter recipient username: ")
    subject = input("Enter subject: ")
    message = input("Enter email message: ")
    if not subject or not message:
        print("Subject and message cannot be empty.")
        return
    if len(subject) > 20:
        print("Subject cannot be more than 20 characters.")
        return
    if len(message) > 50:
        print("Message body cannot be more than 50 characters.")
        return
    emails = load_json(emails_file) or []
    email = {
        "sender": username,
        "recipient": recipient,
        "subject": subject,
        "message": message,
        "timestamp": now()
    }
    emails.append(email)
    try:
        with open(emails_file, 'w') as f:
            json.dump(emails, f, indent=2)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
def view_emails(username):
    print(f"Your Emails")
    emails = load_json(emails_file)
    if not emails:
        print("No emails found.")
        return
    found = False
    for email in emails:
        if email.get('recipient') == username:
            print(f"From: {email.get('sender', 'Unknown')}")
            print(f"Subject: {email.get('subject', 'No Subject')}")
            print(f"Message: {email.get('message', '')}")
            print(f"Time: {email.get('timestamp', '')}")
            found = True
    if not found:
        print("No emails for you.")
def auditor_view_all(filename, label):
    print(f"{label}")
    try:
        data = load_json(filename)
        if data:
            for record in data:
                print(record)
        else:
            print(f"No {label.lower()} found.")
    except Exception as e:
        print(f"Error viewing {label}: {e}")
def auditor_search_user(username):
    print(f" Messages for {username}")
    messages = load_json(messages_file)
    if not messages:
        print("No messages found.")
        return
    found = False
    for msg in messages:
        if msg.get('sender') == username or msg.get('recipient') == username:
            print(f"[{msg.get('timestamp')}] From: {msg.get('sender')} -> To: {msg.get('recipient')}")
            print(f"Message: {msg.get('content', '')}")
            found = True
    if not found:
        print(f"No messages found for {username}")
def search_email_user():
    search_username = input("Enter username to search emails: ")
    emails = load_json(emails_file)
    if not emails:
        print("No emails found.")
        return
    print(f"Emails for {search_username}")
    found = False
    for email in emails:
        if email.get('sender') == search_username or email.get('recipient') == search_username:
            print(f"From: {email.get('sender')}, To: {email.get('recipient')}")
            print(f"Subject: {email.get('subject')}")
            print(f"Message: {email.get('message')}")
            print(f"Time: {email.get('timestamp')}")
            found = True
    if not found:
        print(f"No emails found for {search_username}")
def search_messages_by_time():
    print("Search Messages by Time Duration")
    start_date = input("Enter start date in (YYYY-MM-DD) format: ")
    start_time = input("Enter start time in (HH:MM) format: ")
    end_date = input("Enter end date in (YYYY-MM-DD) format: ")
    end_time = input("Enter end time in (HH:MM) format: ")
    try:
        start_datetime = datetime.strptime(f"{start_date} {start_time}:00", "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(f"{end_date} {end_time}:59", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date/time format. Please use YYYY-MM-DD HH:MM format")
        return
    messages = load_json(messages_file)
    if not messages:
        print("No messages found.")
        return
    found = False
    print(f"Messages between {start_datetime} and {end_datetime}:")
    for msg in messages:
        try:
            msg_datetime = datetime.strptime(msg.get('timestamp'), "%Y-%m-%d %H:%M:%S")
            if start_datetime <= msg_datetime <= end_datetime:
                print(f"[{msg.get('timestamp')}] From: {msg.get('sender')} To: {msg.get('recipient')}")
                print(f"Message: {msg.get('content')}")
                found = True
        except ValueError:
            continue
    if not found:
        print("No messages found in the specified time duration.")
def count_user_messages():
    username = input("Enter username to count messages for: ")
    messages = load_json(messages_file)
    if not messages:
        print("No messages found.")
        return
    to_user = len([m for m in messages if m.get('recipient') == username])
    from_user = len([m for m in messages if m.get('sender') == username])
    total = to_user + from_user
    print(f"Message Count for '{username}':")
    print(f"Messages TO {username}: {to_user}")
    print(f"Messages FROM {username}: {from_user}")
    print(f"Total messages (to and from): {total}")
def view_login_history():
    try:
        history = load_json(history_file)
        if history:
            print("Login History")
            for record in history:
                print(f"User: {record.get('username')}, Action: {record.get('action')}, Time: {record.get('timestamp')}")
        else:
            print("No login history found.")
    except Exception as e:
        print(f"Error: {e}")
def auditor_menu(username):
    while True:
        print(f"Auditor Menu ({username})")
        print("1. View All Messages  2.View All Emails  3.Search User Messages  4.Search User Emails  5.View Login History  6.Search Messages by Time Duration  7.Count Messages to and from a User  8.Manage Users  9.Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            auditor_view_all(messages_file, "All Messages")
        elif choice == '2':
            auditor_view_all(emails_file, "All Emails")
        elif choice == '3':
            search_user = input("Enter username to search:")
            auditor_search_user(search_user)
        elif choice == '4':
            search_email_user()
        elif choice == '5':
            view_login_history()
        elif choice == '6':
            search_messages_by_time()
        elif choice == '7':
            count_user_messages()
        elif choice == '8':
            admin_manage_users()
        elif choice == '9':
            log_history(username, "LOGOUT")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    init_system()
    while True:
        user = login()
        if user:
            if user['role'] == 'student':
                student_menu(user['username'])
            elif user['role'] == 'auditor':
                auditor_menu(user['username'])
            logout(user['username'])
        else:
            try_again = input("Try again? ( press yes or no) ")
            if try_again.lower() != 'yes':
                print("Goodbye!")
                break                                                                                                                    
                                                                                                