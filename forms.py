from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, equal_to
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    email = EmailField("Add Your Email", validators=[DataRequired()])
    username = StringField("Add Username", validators=[DataRequired()])
    password = PasswordField("Your Password", validators=[DataRequired(), Length(min=6, max=12)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), equal_to("password",
                                                                                            message="Passwords Must Be Equal")])
    register = SubmitField("Register/Sign-Up")


class LoginForm(FlaskForm):
    username = StringField("Add Username", validators=[DataRequired()])
    password = PasswordField("Your Password", validators=[DataRequired()])

    login = SubmitField("Log-In")


class EditUserForm(FlaskForm):
    username = StringField("Change Username")
    password = StringField("Change Password", validators=[Length(min=6, max=12)])
    save = SubmitField("Done")


class UploadProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = StringField("Product Price (ONLY NUMBERS NOTHING ELSE)", validators=[DataRequired()])
    image = FileField("Add Prod-Image", validators=[FileRequired()])
    add = SubmitField("Add Product")


class CommentsForm(FlaskForm):
    comment = StringField("Add Your Comment", validators=[Length(min=5, max=80)])
    submit = SubmitField("Comment")

