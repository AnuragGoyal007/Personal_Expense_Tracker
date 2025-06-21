import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from models import db, User, Expense
from forms import RegisterForm, LoginForm, ExpenseForm, BudgetForm, ProfileForm, ChangePasswordForm, ChangeBudgetForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import io
import datetime
from datetime import date

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route("/")
def home():
    return redirect(url_for('dashboard'))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password, budget=form.budget.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login.", "success")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = ExpenseForm()

    # Set default date to today if not submitted
    if request.method == "GET" or not form.validate_on_submit():
        if not form.date.data:
            form.date.data = date.today()

    if form.validate_on_submit():
        new_expense = Expense(
            user_id=current_user.id,
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data,
            date=form.date.data
        )
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added!", "success")
        return redirect(url_for('dashboard'))

    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    total_spent = sum(e.amount for e in expenses)
    over_budget = total_spent > current_user.budget if current_user.budget else False

    # Prepare data for Chart.js
    df = pd.DataFrame([(e.category, e.amount) for e in expenses], columns=["Category", "Amount"])
    chart_data = df.groupby("Category")["Amount"].sum().to_dict()

    return render_template("dashboard.html", form=form, expenses=expenses,
                        total_spent=total_spent, budget=current_user.budget, over_budget=over_budget, chart_data=chart_data)

@app.route("/export")
@login_required
def export():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    df = pd.DataFrame([{
        "Date": e.date,
        "Category": e.category,
        "Amount": e.amount,
        "Description": e.description
    } for e in expenses])
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv",
                    download_name="expenses.csv", as_attachment=True)

@app.route("/edit_expense/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.category = form.category.data
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.date = form.date.data
        db.session.commit()
        flash("Expense updated!", "success")
        return redirect(url_for('dashboard'))
    return render_template("edit_expense.html", form=form, expense=expense)

@app.route("/delete_expense/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted!", "success")
    return redirect(url_for('dashboard'))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    password_form = ChangePasswordForm()
    budget_form = ChangeBudgetForm(obj=current_user)
    if request.method == "POST":
        if 'submit_budget' in request.form and budget_form.validate_on_submit():
            if not check_password_hash(current_user.password, budget_form.password.data):
                flash("Current password is incorrect.", "danger")
            else:
                current_user.budget = budget_form.budget.data
                db.session.commit()
                flash("Budget updated!", "success")
                return redirect(url_for('profile'))
        elif 'submit_password' in request.form and password_form.validate_on_submit():
            if not check_password_hash(current_user.password, password_form.old_password.data):
                flash("Current password is incorrect.", "danger")
            elif password_form.new_password.data != password_form.confirm_password.data:
                flash("New passwords do not match.", "danger")
            else:
                current_user.password = generate_password_hash(password_form.new_password.data)
                db.session.commit()
                flash("Password changed successfully!", "success")
                return redirect(url_for('profile'))
    return render_template("profile.html", password_form=password_form, budget_form=budget_form)

# Initialize DB
with app.app_context():
    db.create_all()
