# **CursedConvo: Real-Time Chat Application**

Welcome to **CursedConvo**, a real-time chat application built with **Django**, **Django Channels**, and **WebSockets**. This project allows multiple users to join a chat room, send messages in real-time, and view a list of online members. The application features a **Discord-like UI**, **username validation**, and a **kickout functionality** for moderators.

---

## **Features**
- **Real-Time Chat:** Send and receive messages instantly using WebSockets.
- **Online Members List:** View a real-time list of users currently online.
- **Username Validation:** Prevent duplicate usernames from joining the chat.
- **Kickout Functionality:** Moderators can kick out users from the chat.
- **Discord-like UI:** A clean and modern dark theme with a responsive design.
- **Message Timestamps:** Each message includes the date and time it was sent.

---

## **Tech Stack**
- **Backend:** Django, Django Channels, Redis
- **Frontend:** HTML, CSS, JavaScript
- **WebSocket Protocol:** Real-time bidirectional communication
- **Deployment:** Daphne (ASGI server)

---

## **Getting Started**

### **Step 1: Clone the Repository**
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/CursedConvo.git
cd CursedConvo
```

---

### **Step 2: Set Up the Virtual Environment**
Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

---

### **Step 3: Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

### **Step 4: Set Up Redis**
1. Install Redis on your machine:
   - **Linux:** `sudo apt-get install redis`
   - **macOS:** `brew install redis`
   - **Windows:** Download Redis from [here](https://github.com/microsoftarchive/redis/releases).

2. Start the Redis server:
   ```bash
   redis-server
   ```

---

### **Step 5: Configure the Application**
1. Update the `CHANNEL_LAYERS` setting in `settings.py` to use Redis:
   ```python
   CHANNEL_LAYERS = {
       "default": {
           "BACKEND": "channels_redis.core.RedisChannelLayer",
           "CONFIG": {
               "hosts": [("127.0.0.1", 6379)],
           },
       },
   }
   ```

2. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

---

### **Step 6: Run the Application**
Start the Django development server with Daphne:
```bash
daphne CursedConvo.asgi:application
```

---

### **Step 7: Access the Application**
Open your browser and navigate to:
```
http://127.0.0.1:8000/chat/
```

---

## **How It Works**

### **1. Join the Chat**
- Enter a unique username to join the chat.
- If the username is already taken, you'll be prompted to choose a different one.

### **2. Send Messages**
- Type your message in the input box and press **Enter** or click **Send**.
- Your message will be broadcast to all users in the chat room.

### **3. View Online Members**
- The list of online members is displayed in the right-hand panel.
- The list updates in real-time as users join or leave the chat.

### **4. Kick Out Users (Moderators Only)**
- Moderators can kick out users by clicking the **Kick Out** button next to their username.
- The kicked user will be disconnected from the chat.

---

## **Project Structure**
```
CursedConvo/
├── chat/                      # Django app for chat functionality
│   ├── consumers.py           # WebSocket consumers
│   ├── routing.py             # WebSocket routing
│   ├── templates/             # HTML templates
│   └── views.py               # Django views
├── CursedConvo/               # Django project settings
│   ├── asgi.py                # ASGI configuration
│   ├── settings.py            # Django settings
│   └── urls.py                # URL routing
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## **Screenshots**
1. **Chat Room:**
   ![Chat Room](screenshots/chat-room.png)

2. **Online Members List:**
   ![Online Members](screenshots/online-members.png)

3. **Username Popup:**
   ![Username Popup](screenshots/username-popup.png)

---

## **Future Enhancements**
- **Message Persistence:** Store chat history in a database.
- **Private Messaging:** Allow users to send private messages to each other.
- **User Roles:** Implement roles like admin, moderator, and user.
- **Emoji Support:** Add emoji picker for messages.

---

## **Contributing**
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**
- **Django Channels:** For enabling WebSocket support in Django.
- **Redis:** For providing a scalable channel layer.
- **Daphne:** For serving the ASGI application.

---

## **Contact**
For any questions or feedback, feel free to reach out:
- **Email:** your.email@example.com
- **GitHub:** [yourusername](https://github.com/yourusername)

---

Happy chatting! 🚀

