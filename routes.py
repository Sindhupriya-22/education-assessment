from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from forms import StudentAssessmentForm
from translations import get_translations
import logging

# Configure logging
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    language = request.args.get('lang', 'en')
    session['language'] = language
    translations = get_translations(language)
    return render_template('index.html', translations=translations, current_language=language)

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    from models import Student  # Deferred import
    form = StudentAssessmentForm()
    language = session.get('language', 'en')
    translations = get_translations(language)
    
    if form.validate_on_submit():
        try:
            # Create new student record
            student = Student(
                name=form.name.data,
                age=form.age.data,
                location=form.location.data,
                education_level=form.education_level.data,
                preferred_language=form.preferred_language.data,
                technical_skills=form.technical_skills.data,
                communication_skills=form.communication_skills.data,
                analytical_skills=form.analytical_skills.data,
                creative_skills=form.creative_skills.data,
                leadership_skills=form.leadership_skills.data,
                interest_technology=form.interest_technology.data,
                interest_arts=form.interest_arts.data,
                interest_business=form.interest_business.data,
                interest_healthcare=form.interest_healthcare.data,
                interest_education=form.interest_education.data,
                interest_agriculture=form.interest_agriculture.data,
                interest_government=form.interest_government.data,
                extroversion=form.extroversion.data,
                conscientiousness=form.conscientiousness.data,
                openness=form.openness.data,
                agreeableness=form.agreeableness.data
            )
            
            db.session.add(student)
            db.session.commit()
            
            # Store student ID in session for results
            session['student_id'] = student.id
            
            # Redirect to results
            return redirect(url_for('results'))
            
        except Exception as e:
            logger.error(f"Error saving student assessment: {str(e)}")
            flash('An error occurred while processing your assessment. Please try again.', 'error')
            db.session.rollback()
    
    return render_template('assessment.html', form=form, translations=translations)

@app.route('/results')
def results():
    from models import Student, Career, Course, Scholarship, CareerRecommendation  # Deferred import
    from ml_model import CareerRecommendationEngine  # Deferred import
    ml_engine = CareerRecommendationEngine()  # Initialize inside function
    student_id = session.get('student_id')
    if not student_id:
        flash('Please complete the assessment first.', 'warning')
        return redirect(url_for('assessment'))
    
    language = session.get('language', 'en')
    translations = get_translations(language)
    
    try:
        student = Student.query.get(student_id)
        if not student:
            flash('Student record not found.', 'error')
            return redirect(url_for('assessment'))
        
        # Get career recommendations
        recommendations = ml_engine.get_career_recommendations(student, top_k=8)
        
        # Save recommendations to database
        for rec in recommendations:
            career_rec = CareerRecommendation(
                student_id=student.id,
                career_id=rec['career'].id,
                match_score=rec['match_score']
            )
            db.session.add(career_rec)
        
        db.session.commit()
        
        # Get courses for top recommendations
        top_career_ids = [rec['career'].id for rec in recommendations[:5]]
        courses = Course.query.filter(Course.career_id.in_(top_career_ids)).all()
        
        # Get scholarships (prioritize rural-friendly ones)
        scholarships = Scholarship.query.filter_by(for_rural_students=True).limit(6).all()
        if len(scholarships) < 6:
            additional_scholarships = Scholarship.query.filter_by(for_rural_students=False).limit(6 - len(scholarships)).all()
            scholarships.extend(additional_scholarships)
        
        return render_template('results.html', 
                             student=student,
                             recommendations=recommendations,
                             courses=courses,
                             scholarships=scholarships,
                             translations=translations)
        
    except Exception as e:
        logger.error(f"Error generating results: {str(e)}")
        flash('An error occurred while generating your results. Please try again.', 'error')
        return redirect(url_for('assessment'))

@app.route('/career/<int:career_id>')
def career_details(career_id):
    from models import Student, Career, Course  # Deferred import
    from ml_model import CareerRecommendationEngine  # Deferred import
    ml_engine = CareerRecommendationEngine()  # Initialize inside function
    language = session.get('language', 'en')
    translations = get_translations(language)
    student_id = session.get('student_id')
    
    career = Career.query.get_or_404(career_id)
    courses = Course.query.filter_by(career_id=career_id).all()
    
    explanation = []
    match_score = 0
    
    if student_id:
        student = Student.query.get(student_id)
        if student:
            explanation = ml_engine.get_explanation(student, career)
            match_score = int(ml_engine.calculate_match_score(student, career) * 100)
    
    return render_template('career_details.html',
                         career=career,
                         courses=courses,
                         explanation=explanation,
                         match_score=match_score,
                         translations=translations)

@app.route('/api/career-chart-data/<int:student_id>')
def career_chart_data(student_id):
    from models import Student  # Deferred import
    from ml_model import CareerRecommendationEngine  # Deferred import
    ml_engine = CareerRecommendationEngine()  # Initialize inside function
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        recommendations = ml_engine.get_career_recommendations(student, top_k=6)
        
        chart_data = {
            'labels': [rec['career'].name for rec in recommendations],
            'data': [rec['match_percentage'] for rec in recommendations],
            'colors': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
        }
        
        return jsonify(chart_data)
        
    except Exception as e:
        logger.error(f"Error generating chart data: {str(e)}")
        return jsonify({'error': 'Failed to generate chart data'}), 500

@app.errorhandler(404)
def not_found_error(error):
    language = session.get('language', 'en')
    translations = get_translations(language)
    return render_template('base.html', translations=translations), 404

@app.errorhandler(500)
def internal_error(error):
    language = session.get('language', 'en')
    translations = get_translations(language)
    db.session.rollback()
    return render_template('base.html', translations=translations), 500