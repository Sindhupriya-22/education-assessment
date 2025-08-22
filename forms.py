from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length

class StudentAssessmentForm(FlaskForm):
    # Basic Information
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=16, max=50)])
    location = StringField('Location (City/Village)', validators=[DataRequired(), Length(min=2, max=100)])
    education_level = SelectField('Education Level', 
                                choices=[
                                    ('10th_grade', '10th Grade'),
                                    ('12th_grade', '12th Grade'),
                                    ('diploma', 'Diploma'),
                                    ('graduate', 'Graduate'),
                                    ('postgraduate', 'Post Graduate')
                                ],
                                validators=[DataRequired()])
    preferred_language = SelectField('Preferred Language',
                                   choices=[
                                       ('en', 'English'),
                                       ('hi', 'Hindi'),
                                       ('te', 'Telugu'),
                                       ('ta', 'Tamil'),
                                       ('bn', 'Bengali'),
                                       ('mr', 'Marathi')
                                   ],
                                   default='en')
    
    # Skills Assessment (1-5 scale)
    technical_skills = RadioField('Technical Skills (Programming, IT, Engineering)',
                                choices=[('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
                                coerce=int, validators=[DataRequired()])
    
    communication_skills = RadioField('Communication Skills (Speaking, Writing, Presentation)',
                                    choices=[('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
                                    coerce=int, validators=[DataRequired()])
    
    analytical_skills = RadioField('Analytical Skills (Problem-solving, Critical thinking)',
                                 choices=[('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
                                 coerce=int, validators=[DataRequired()])
    
    creative_skills = RadioField('Creative Skills (Art, Design, Innovation)',
                               choices=[('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
                               coerce=int, validators=[DataRequired()])
    
    leadership_skills = RadioField('Leadership Skills (Team management, Decision making)',
                                 choices=[('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
                                 coerce=int, validators=[DataRequired()])
    
    # Interest Assessment (1-5 scale)
    interest_technology = RadioField('Interest in Technology & Computing',
                                   choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very High')],
                                   coerce=int, validators=[DataRequired()])
    
    interest_arts = RadioField('Interest in Arts & Creative Fields',
                             choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very High')],
                             coerce=int, validators=[DataRequired()])
    
    interest_business = RadioField('Interest in Business & Entrepreneurship',
                                 choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very High')],
                                 coerce=int, validators=[DataRequired()])
    
    interest_healthcare = RadioField('Interest in Healthcare & Medicine',
                                   choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very High')],
                                   coerce=int, validators=[DataRequired()])
    
    interest_education = RadioField('Interest in Education & Teaching',
                                  choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very High')],
                                  coerce=int, validators=[DataRequired()])
    
    interest_agriculture = RadioField('Interest in Agriculture & Rural Development',
                                    choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very High')],
                                    coerce=int, validators=[DataRequired()])
    
    interest_government = RadioField('Interest in Government & Public Service',
                                   choices=[('1', 'Very Low'), ('2', 'Low'), ('3', 'Moderate'), ('4', 'High'), ('5', 'Very High')],
                                   coerce=int, validators=[DataRequired()])
    
    # Personality Assessment (1-5 scale)
    extroversion = RadioField('I enjoy working with people and in teams',
                            choices=[('1', 'Strongly Disagree'), ('2', 'Disagree'), ('3', 'Neutral'), ('4', ' Agree'), ('5', 'Strongly Agree')],
                            coerce=int, validators=[DataRequired()])
    
    conscientiousness = RadioField('I am organized and detail-oriented',
                                 choices=[('1', 'Strongly Disagree'), ('2', 'Disagree'), ('3', 'Neutral'), ('4', ' Agree'), ('5', 'Strongly Agree')],
                                 coerce=int, validators=[DataRequired()])
    
    openness = RadioField('I enjoy learning new things and trying new experiences',
                        choices=[('1', 'Strongly Disagree'), ('2', 'Disagree'), ('3', 'Neutral'), ('4', ' Agree'), ('5', 'Strongly Agree')],
                        coerce=int, validators=[DataRequired()])
    
    agreeableness = RadioField('I prefer cooperation over competition',
                             choices=[('1', 'Strongly Disagree'), ('2', 'Disagree'), ('3', 'Neutral'), ('4', ' Agree'), ('5', 'Strongly Agree')],
                             coerce=int, validators=[DataRequired()])