from app import db

def load_initial_data():
    """Load initial career data, courses, and scholarships"""
    # Import models here to avoid circular import
    from models import Career, Course, Scholarship

    # Check if data already exists
    if Career.query.count() > 0:
        return

    # Career data with realistic requirements and alignments
    careers_data = [
        {
            'name': 'Software Developer',
            'description': 'Design, develop, and maintain software applications and systems.',
            'category': 'Technology',
            'technical_weight': 0.9,
            'communication_weight': 0.6,
            'analytical_weight': 0.8,
            'creative_weight': 0.7,
            'leadership_weight': 0.3,
            'technology_alignment': 0.9,
            'arts_alignment': 0.3,
            'business_alignment': 0.4,
            'healthcare_alignment': 0.1,
            'education_alignment': 0.2,
            'agriculture_alignment': 0.1,
            'government_alignment': 0.2,
            'extroversion_fit': 0.3,
            'conscientiousness_fit': 0.8,
            'openness_fit': 0.9,
            'agreeableness_fit': 0.4,
            'average_salary': '₹4-12 LPA',
            'job_growth': 'High (20%+ annually)',
            'education_required': 'Engineering/BCA/MCA',
            'rural_opportunities': True
        },
        {
            'name': 'Digital Marketing Specialist',
            'description': 'Plan and execute digital marketing campaigns across various online platforms.',
            'category': 'Business',
            'technical_weight': 0.6,
            'communication_weight': 0.9,
            'analytical_weight': 0.7,
            'creative_weight': 0.8,
            'leadership_weight': 0.5,
            'technology_alignment': 0.6,
            'arts_alignment': 0.7,
            'business_alignment': 0.9,
            'healthcare_alignment': 0.1,
            'education_alignment': 0.3,
            'agriculture_alignment': 0.2,
            'government_alignment': 0.2,
            'extroversion_fit': 0.8,
            'conscientiousness_fit': 0.7,
            'openness_fit': 0.8,
            'agreeableness_fit': 0.6,
            'average_salary': '₹3-8 LPA',
            'job_growth': 'Very High (25%+ annually)',
            'education_required': 'Graduate + Digital Marketing Course',
            'rural_opportunities': True
        },
        {
            'name': 'Primary School Teacher',
            'description': 'Educate and nurture young minds in primary education settings.',
            'category': 'Education',
            'technical_weight': 0.2,
            'communication_weight': 0.9,
            'analytical_weight': 0.5,
            'creative_weight': 0.7,
            'leadership_weight': 0.8,
            'technology_alignment': 0.3,
            'arts_alignment': 0.6,
            'business_alignment': 0.2,
            'healthcare_alignment': 0.2,
            'education_alignment': 0.9,
            'agriculture_alignment': 0.1,
            'government_alignment': 0.4,
            'extroversion_fit': 0.8,
            'conscientiousness_fit': 0.9,
            'openness_fit': 0.7,
            'agreeableness_fit': 0.9,
            'average_salary': '₹2-4 LPA',
            'job_growth': 'Stable (5-10% annually)',
            'education_required': 'B.Ed or D.Ed',
            'rural_opportunities': True
        },
        {
            'name': 'Agricultural Technician',
            'description': 'Assist farmers with modern farming techniques and crop management.',
            'category': 'Agriculture',
            'technical_weight': 0.6,
            'communication_weight': 0.7,
            'analytical_weight': 0.6,
            'creative_weight': 0.4,
            'leadership_weight': 0.5,
            'technology_alignment': 0.5,
            'arts_alignment': 0.2,
            'business_alignment': 0.3,
            'healthcare_alignment': 0.2,
            'education_alignment': 0.4,
            'agriculture_alignment': 0.9,
            'government_alignment': 0.3,
            'extroversion_fit': 0.6,
            'conscientiousness_fit': 0.8,
            'openness_fit': 0.6,
            'agreeableness_fit': 0.7,
            'average_salary': '₹2-5 LPA',
            'job_growth': 'Growing (10-15% annually)',
            'education_required': 'Diploma in Agriculture',
            'rural_opportunities': True
        },
        {
            'name': 'Healthcare Worker (ASHA)',
            'description': 'Provide primary healthcare services in rural communities.',
            'category': 'Healthcare',
            'technical_weight': 0.4,
            'communication_weight': 0.8,
            'analytical_weight': 0.5,
            'creative_weight': 0.3,
            'leadership_weight': 0.6,
            'technology_alignment': 0.2,
            'arts_alignment': 0.2,
            'business_alignment': 0.2,
            'healthcare_alignment': 0.9,
            'education_alignment': 0.5,
            'agriculture_alignment': 0.2,
            'government_alignment': 0.7,
            'extroversion_fit': 0.8,
            'conscientiousness_fit': 0.9,
            'openness_fit': 0.6,
            'agreeableness_fit': 0.9,
            'average_salary': '₹1.5-3 LPA',
            'job_growth': 'Stable (5-8% annually)',
            'education_required': '12th Grade + Health Training',
            'rural_opportunities': True
        },
        {
            'name': 'Graphic Designer',
            'description': 'Create visual concepts and designs for various media and platforms.',
            'category': 'Arts & Design',
            'technical_weight': 0.7,
            'communication_weight': 0.6,
            'analytical_weight': 0.5,
            'creative_weight': 0.9,
            'leadership_weight': 0.3,
            'technology_alignment': 0.6,
            'arts_alignment': 0.9,
            'business_alignment': 0.5,
            'healthcare_alignment': 0.1,
            'education_alignment': 0.2,
            'agriculture_alignment': 0.1,
            'government_alignment': 0.2,
            'extroversion_fit': 0.4,
            'conscientiousness_fit': 0.7,
            'openness_fit': 0.9,
            'agreeableness_fit': 0.5,
            'average_salary': '₹2-6 LPA',
            'job_growth': 'Growing (12-15% annually)',
            'education_required': 'Diploma/Degree in Design',
            'rural_opportunities': True
        }
    ]

    for career_data in careers_data:
        career = Career(**career_data)
        db.session.add(career)

    # Course data
    courses_data = [
        {
            'title': 'Python Programming',
            'provider': 'Coursera',
            'url': 'https://www.coursera.org/learn/python',
            'description': 'Learn Python programming basics',
            'duration': '6 weeks',
            'level': 'Beginner',
            'is_free': True,
            'career_id': 1  # Software Developer
        },
        {
            'title': 'Digital Marketing Fundamentals',
            'provider': 'Google',
            'url': 'https://learndigital.withgoogle.com/digitalgarage/course/digital-marketing',
            'description': 'Master digital marketing basics',
            'duration': '40 hours',
            'level': 'Beginner',
            'is_free': True,
            'career_id': 2  # Digital Marketing Specialist
        },
        {
            'title': 'Introduction to Teaching',
            'provider': 'Alison',
            'url': 'https://alison.com/course/introduction-to-teaching',
            'description': 'Learn foundational teaching skills',
            'duration': '3-4 hours',
            'level': 'Beginner',
            'is_free': True,
            'career_id': 3  # Primary School Teacher
        },
        {
            'title': 'Modern Farming Techniques',
            'provider': 'FAO e-learning Academy',
            'url': 'https://elearning.fao.org/',
            'description': 'Learn sustainable farming practices',
            'duration': '8 weeks',
            'level': 'Intermediate',
            'is_free': True,
            'career_id': 4  # Agricultural Technician
        },
        {
            'title': 'Community Healthcare',
            'provider': 'FutureLearn',
            'url': 'https://www.futurelearn.com/courses/community-healthcare',
            'description': 'Training for community health workers',
            'duration': '6 weeks',
            'level': 'Beginner',
            'is_free': True,
            'career_id': 5  # Healthcare Worker (ASHA)
        },
        {
            'title': 'Graphic Design Basics',
            'provider': 'Canva Design School',
            'url': 'https://designschool.canva.com/',
            'description': 'Learn design principles and tools',
            'duration': '4 weeks',
            'level': 'Beginner',
            'is_free': True,
            'career_id': 6  # Graphic Designer
        }
    ]

    for course_data in courses_data:
        course = Course(**course_data)
        db.session.add(course)

    # Scholarship data
    scholarships_data = [
        {
            'name': 'National Scholarship Portal - Merit Cum Means',
            'provider': 'Government of India',
            'description': 'Merit-cum-means scholarship for students from economically weaker sections',
            'amount': '₹10,000 - ₹20,000 per year',
            'eligibility': 'Students with family income less than ₹2.5 LPA',
            'application_url': 'https://scholarships.gov.in/',
            'deadline': 'October 31st (Annual)',
            'for_rural_students': True
        },
        {
        'name': 'Post Matric Scholarship for SC Students',
        'provider': 'Ministry of Social Justice & Empowerment',
        'description': 'Financial assistance for SC students pursuing higher education',
        'amount': '₹5,000 – ₹25,000 per year',
        'eligibility': 'SC category students with family income < ₹2.5 LPA',
        'application_url': 'https://https://socialjustice.gov.in/',
        'deadline': 'November 30th (Annual)',
        'for_rural_students': True
        },
        {
            'name': 'INSPIRE Scholarship',
            'provider': 'Department of Science & Technology',
            'description': 'For students pursuing science courses',
            'amount': '₹80,000 per year',
            'eligibility': 'Top students in 12th board exams studying science',
            'application_url': 'https://online-inspire.gov.in/',
            'deadline': 'July 31st (Annual)',
            'for_rural_students': True
        },
        {
            'name': 'Kishore Vaigyanik Protsahan Yojana (KVPY)',
            'provider': 'Indian Institute of Science',
            'description': 'Fellowship for students with science aptitude',
            'amount': '₹5,000 - ₹7,000 per month',
            'eligibility': 'Students in 11th, 12th, and 1st year of science courses',
            'application_url': 'http://www.kvpy.iisc.ernet.in/',
            'deadline': 'July 15th (Annual)',
            'for_rural_students': False
        },
        {
            'name': 'Pragati Scholarship for Girls',
            'provider': 'AICTE',
            'description': 'Technical education support for girl students',
            'amount': '₹30,000 per year + ₹2,000 for books',
            'eligibility': 'Girl students in technical courses, family income < ₹8 LPA',
            'application_url': 'https://www.aicte-india.org/schemes/students-development-schemes/pragati-scholarship-scheme',
            'deadline': 'December 31st (Annual)',
            'for_rural_students': True
        },
        {
            'name': 'Means Cum Merit Scholarship',
            'provider': 'UGC',
            'description': 'Support for undergraduate and postgraduate students',
            'amount': '₹5,000 - ₹10,000 per year',
            'eligibility': 'Students with good academic record and family income < ₹6 LPA',
            'application_url': 'https://www.youthforseva.org/NMMS?emulatemode=1&https://www.youthforseva.org/Volunteer&gad_source=1&gad_campaignid=15728408129&gbraid=0AAA',
            'deadline': 'September 30th (Annual)',
            'for_rural_students': True
        },
        {
            'name': 'Prime Minister Research Fellowship',
            'provider': 'Ministry of Education',
            'description': 'For PhD students in IITs, IISc, and other premier institutes',
            'amount': '₹70,000 - ₹80,000 per month',
            'eligibility': 'BTech/MTech students with high CGPA',
            'application_url': 'https://www.pmrf.in/',
            'deadline': 'May 31st and September 30th',
            'for_rural_students': False
        },
        {
            'name': 'Swami Vivekananda Single Girl Child Scholarship',
            'provider': 'UGC',
            'description': 'Support for single girl child pursuing higher education',
            'amount': '₹30,000 per year',
            'eligibility': 'Single girl child pursuing postgraduate studies',
            'application_url': 'https://www.myscheme.gov.in',
            'deadline': 'October 31st (Annual)',
            'for_rural_students': True
        }
    ]

    for scholarship_data in scholarships_data:
        scholarship = Scholarship(**scholarship_data)
        db.session.add(scholarship)

    # Commit all changes
    db.session.commit()
    print("Initial data loaded successfully!")