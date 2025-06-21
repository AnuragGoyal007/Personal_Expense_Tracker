# 💰 Expense Tracker - A Full-Stack Web Application

A modern, responsive web application for tracking personal expenses, with user authentication, budgeting, data visualization, and more. Built with Flask, PostgreSQL, and Bootstrap, and deployed on Vercel.

**Live Demo:** [Link to your Vercel deployment] (You can add this after deploying!)

## ✨ Features

- **User Authentication:** Secure registration and login.
- **Profile Management:** Users can update their password.
- **Expense Tracking:** Full CRUD (Create, Read, Update, Delete) for expenses.
- **Budgeting:** Set a monthly budget and see how you're tracking.
- **Interactive Dashboard:**
  - Visualize expense breakdown with a Google Pie Chart.
  - See quick stats: biggest expense, most frequent category.
  - Dark mode for a comfortable user experience.
- **Responsive Design:** Looks great on desktop, tablet, and mobile.
- **Data Export:** Export your expenses as a CSV file.
- **Modern UI:** Built with Bootstrap, custom CSS, and modals for a clean, user-friendly experience.

## 🛠️ Tech Stack

- **Backend:**
  - Python
  - Flask (web framework)
  - PostgreSQL (database)
  - Flask-Login (user authentication)
  - Flask-WTF (forms and security)
  - Werkzeug (password hashing)
- **Frontend:**
  - HTML
  - CSS
  - Bootstrap
  - JavaScript
  - Google Charts (data visualization)
- **Deployment:**
  - Vercel
  - Git & GitHub

## 🚀 How to Run Locally

### **Prerequisites**
- Python 3.x
- Git

### **Setup**
1. **Clone the repository:**
   ```sh
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```
2. **Create a virtual environment:**
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows, use: env\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up your database:**
   - For SQLite (local):  
     No setup needed, it will be created automatically.
   - For PostgreSQL (recommended):
     - Create a `.env` file with `DATABASE_URL=your_postgres_url`
     - Make sure `python-dotenv` is in `requirements.txt`
5. **Run the app:**
   ```sh
   flask run
   ```
   Or, for Vercel dev:
   ```sh
   vercel dev
   ```
   Open `http://127.0.0.1:5000` in your browser.

## 📸 Screenshots

(Optional: Add screenshots of your dashboard, login page, and profile page here.)

## 📝 What I Learned

- Building a full-stack application from scratch.
- Implementing secure user authentication and session management.
- Designing a responsive and modern UI with Bootstrap and custom CSS.
- Working with a relational database (PostgreSQL/SQLite) and ORM (Flask-SQLAlchemy).
- Deploying a Python web app on a modern cloud platform (Vercel).

---
*Feel free to connect with me if you have any questions!*
(Optional: Add your LinkedIn/portfolio link here.) 