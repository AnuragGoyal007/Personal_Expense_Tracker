from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField("Password", validators=[DataRequired()])
    budget = FloatField("Monthly Budget", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ExpenseForm(FlaskForm):
    category = SelectField("Category", choices=["Food", "Travel", "Bills", "Shopping", "Health", "Misc"], validators=[DataRequired()])
    amount = FloatField("Amount", validators=[DataRequired()])
    description = TextAreaField("Description")
    date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Add Expense")

class BudgetForm(FlaskForm):
    budget = FloatField("Monthly Budget", validators=[DataRequired()])
    submit = SubmitField("Set Budget")

class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField("Update Profile")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired()])
    submit_password = SubmitField("Change Password")

class ChangeBudgetForm(FlaskForm):
    budget = FloatField("Monthly Budget", validators=[DataRequired()])
    password = PasswordField("Current Password", validators=[DataRequired()])
    submit_budget = SubmitField("Change Budget")
