# Social Media API

📖 **Overview**  
The **Social Media API** project is a backend application built with Django Rest Framework (DRF) to implement key features seen in social media platforms. It focuses on scalable API design and demonstrates functionalities like user authentication, notifications, posts, and interactions.

---

🛠 **Features**  
- **User Accounts**:
  - Registration and authentication.
  - User profile management.
- **Posts**:
  - CRUD operations for posts (Create, Read, Update, Delete).
  - Like and comment functionalities.
- **Notifications**:
  - Real-time notifications for interactions (e.g., likes, comments).
- **Static Files**:
  - Configuration for serving media and other static assets.
- **Database**:
  - SQLite as default for development.

---

📂 **Project Structure**  
- **`accounts/`**:
  Handles user authentication, profile management, and user permissions.
- **`notifications/`**:
  Implements notifications for likes and comments on posts.
- **`posts/`**:
  Manages post creation, modification, and interaction logic.
- **`social_media_api/`**:
  Main application settings and configurations.
- **`staticfiles/`**:
  Stores and serves CSS, JavaScript, and media assets.
- **Database Files**:
  - `db.sqlite3` for storing data (can be replaced with other production-ready databases like PostgreSQL).
- **Additional Files**:
  - `requirements.txt`: Lists project dependencies.
  - `Procfile`: Configurations for deploying to platforms like Heroku.
  - `runtime.txt`: Specifies the runtime environment.

---

💡 **How to Use**  
### 1. Clone the Repository:
```bash
git clone https://github.com/Ratim001/Alx_DjangoLearnLab.git