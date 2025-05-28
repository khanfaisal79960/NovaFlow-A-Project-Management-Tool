# NovaFlow: Streamline Your Projects, Unleash Your Potential

*A glimpse of the NovaFlow project dashboard.*

NovaFlow is a lightweight, web-based project management tool designed to help individuals and small teams organize their projects and tasks efficiently. It provides a clean, intuitive interface for tracking project progress, managing tasks, and collaborating within teams.

---

## ✨ Features

### 🔐 User Authentication
- Secure user registration and login/logout functionality.

### 📁 Project Management
- Create, view, edit, and delete projects.
- Projects can be personal or associated with a team.
- Track project progress with customizable statuses:
  `Not Started`, `Planning`, `In Progress`, `Testing`, `Completed`, `On Hold`, `Cancelled`.

### ✅ Task Management
- Add, view, edit, and delete tasks within each project.
- Mark tasks as complete or pending.
- Tasks inherit team association from their parent project.

### 👥 Team Collaboration
- Create new teams or join existing ones using a unique Team ID.
- View members of a team.
- Projects can be assigned to teams, allowing team members to access and manage them.

### 💻 Responsive Design
- Built with Tailwind CSS for a modern, mobile-friendly interface.

### 📝 Markdown Support
- Project and task descriptions support Markdown formatting.

### ❌ Custom 404 Page
- A friendly custom page for non-existent routes.

---

## 🛠️ Technologies Used

### Backend
- **Flask** – Lightweight Python web framework.
- **Werkzeug** – Provides password hashing and security utilities.
- **Markdown** – Python library for converting Markdown to HTML.

### Frontend
- **Jinja2** – Flask's templating engine.
- **Tailwind CSS** – Utility-first CSS framework for rapid UI development.
- **Markdown-it** – JavaScript Markdown parser for optional client-side rendering.
- **Font Awesome** – Icon library for various UI elements.

---

## 🚀 Getting Started

### ✅ Prerequisites
Make sure you have Python 3.8+ and pip installed.

### 📦 Installation

```bash
git clone https://github.com/your-username/NovaFlow.git
cd NovaFlow

# Create and activate virtual environment
python -m venv venv

# On Windows
.env\Scriptsctivate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the Application

Ensure your virtual environment is active, then run the following command:

```bash
python app.py
```

Now, open your browser and go to:

```text
http://127.0.0.1:5000/
```

> **Note:** The `app.py` file includes `_initialize_test_data()` which adds a sample user and team. Remove or comment out this function before deploying to production.

---

## 🌐 Live Project

Access the live demo: [NovaFlow Live](https://nova-flow-a-project-management-tool.vercel.app/landing)

---

## 📸 Project Screenshots
![Alt Text](./assets/screenshot_1.jpg)
![Alt Text](./assets/screenshot_2.jpg)
![Alt Text](./assets/screenshot_3.jpg)
![Alt Text](./assets/screenshot_4.jpg)
![Alt Text](./assets/screenshot_5.jpg)

---

## 💡 Usage Guide

### 🧑‍💻 Sign Up / Log In

Register a new account or log in with existing credentials.

### 👨‍👩‍👧‍👦 Teams

- Navigate to the **Teams** tab.
- **Create** a team and share the **Team ID**.
- **Join** existing teams by entering a valid **Team ID**.

### 📂 Projects

- Add a new project with a name, description (Markdown supported), team (optional), and status.
- View, edit, and delete your projects.

### 📋 Tasks

- Add, edit, delete, and mark tasks as complete/incomplete inside any project.

---

## 🤝 Contributing

This project is a personal endeavor, but feel free to fork the repository, experiment, and suggest improvements via pull requests.

---

## 📧 Contact & Socials

- **Portfolio:** [khanfaisal.netlify.app](https://khanfaisal.netlify.app)
- **GitHub:** [github.com/khanfaisal79960](https://github.com/khanfaisal79960)
- **LinkedIn:** [linkedin.com/in/khanfaisal79960](https://www.linkedin.com/in/khanfaisal79960)
- **Instagram:** [@mr._perfect_1004](https://instagram.com/mr._perfect_1004)
- **Medium:** [@khanfaisal79960](https://medium.com/@khanfaisal79960)
