from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, FloatField, SelectField, IntegerField, TextAreaField, Form, BooleanField, SelectMultipleField, FieldList, FormField
from wtforms.validators import Email, Length, InputRequired, NumberRange, Optional, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput, TextInput

class RegForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20)])
    name = StringField('Name')

class AuthorEntryForm(Form): # Note: This inherits from wtforms.Form, not FlaskForm
    author_name = StringField("Author Name", validators=[Optional(), Length(max=50)])
    is_illustrator = BooleanField('Illustrator')

class BookForm(FlaskForm):
    genres = SelectMultipleField(
        'Choose multiple Genres:',
        # Custom widgets to render as a list of checkboxes
        #widget=ListWidget(prefix_label=False), # False means labels are not wrapped in <li>
        choices=[], # Choices will be set dynamically in the route
        
    )

    def validate_genres(self, field):
        """
        Custom validator to ensure at least one genre is selected
        """
        if not field.data:
            raise ValidationError("Please select at least on genre")

    title = StringField('Title:', validators=[InputRequired(), Length(max=100)])

    category = SelectField(
        'Choose a category:',
        choices=[
            ('Adult', 'Adult'),
            ('Teens', 'Teens'),
            ('Children', 'Children')
        ],
        validators=[InputRequired()]
    )

    url = StringField('URL for Cover:', validators=[Optional()])

    description = TextAreaField('Description:', validators=[Optional()])

    # 6. "Author 1:, Author 2:, ..." with "Illustrator" checkbox
    # This requires a FieldList of AuthorEntryForm
    authors = FieldList(
        FormField(AuthorEntryForm),
        min_entries=5, # Always show at least one author field
        max_entries=5, # Limit to 5 author fields as per your design
        label='Authors' # A general label, might be omitted in rendering
    )

    def validate_authors(self, field):
        has_author = any(entry.author_name.data and entry.author_name.data.strip() for entry in field.entries)
        if not has_author:
            raise ValidationError("Book needs at least 1 author")

    pages = IntegerField('Number of pages:', validators=[InputRequired(), NumberRange(min=1)])

    copies = IntegerField('Number of copies:', validators=[InputRequired(), NumberRange(min=1)])