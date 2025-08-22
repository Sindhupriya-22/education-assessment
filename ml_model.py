import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from models import Career, Student
import logging

class CareerRecommendationEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_match_score(self, student, career):
        """
        Calculate match score between student and career using weighted similarity
        """
        try:
            # Normalize student skills and interests to 0-1 scale
            student_skills = np.array([
                student.technical_skills / 5.0,
                student.communication_skills / 5.0,
                student.analytical_skills / 5.0,
                student.creative_skills / 5.0,
                student.leadership_skills / 5.0
            ])
            
            student_interests = np.array([
                student.interest_technology / 5.0,
                student.interest_arts / 5.0,
                student.interest_business / 5.0,
                student.interest_healthcare / 5.0,
                student.interest_education / 5.0,
                student.interest_agriculture / 5.0,
                student.interest_government / 5.0
            ])
            
            student_personality = np.array([
                student.extroversion / 5.0,
                student.conscientiousness / 5.0,
                student.openness / 5.0,
                student.agreeableness / 5.0
            ])
            
            # Career requirements and alignments
            career_skills_req = np.array([
                career.technical_weight,
                career.communication_weight,
                career.analytical_weight,
                career.creative_weight,
                career.leadership_weight
            ])
            
            career_interest_align = np.array([
                career.technology_alignment,
                career.arts_alignment,
                career.business_alignment,
                career.healthcare_alignment,
                career.education_alignment,
                career.agriculture_alignment,
                career.government_alignment
            ])
            
            career_personality_fit = np.array([
                career.extroversion_fit,
                career.conscientiousness_fit,
                career.openness_fit,
                career.agreeableness_fit
            ])
            
            # Calculate weighted scores
            skills_score = self._calculate_skills_match(student_skills, career_skills_req)
            interests_score = self._calculate_dot_product_similarity(student_interests, career_interest_align)
            personality_score = self._calculate_personality_fit(student_personality, career_personality_fit)
            
            # Weighted final score
            final_score = (
                0.4 * skills_score +
                0.4 * interests_score +
                0.2 * personality_score
            )
            
            # Boost score for rural-friendly careers
            if career.rural_opportunities:
                final_score *= 1.1
            
            return min(final_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Error calculating match score: {str(e)}")
            return 0.0
    
    def _calculate_skills_match(self, student_skills, career_requirements):
        """
        Calculate how well student skills match career requirements
        """
        # Use weighted similarity where higher career requirements demand higher student skills
        weighted_matches = []
        
        for i in range(len(student_skills)):
            if career_requirements[i] > 0:
                # For required skills, student should meet the requirement
                skill_match = min(student_skills[i] / career_requirements[i], 1.0)
                weighted_matches.append(skill_match * career_requirements[i])
            else:
                # For non-required skills, any level is acceptable
                weighted_matches.append(student_skills[i] * 0.1)
        
        return np.mean(weighted_matches) if weighted_matches else 0.0
    
    def _calculate_dot_product_similarity(self, student_vector, career_vector):
        """
        Calculate similarity using dot product (measures alignment)
        """
        return np.dot(student_vector, career_vector) / (len(student_vector))
    
    def _calculate_personality_fit(self, student_personality, career_personality_fit):
        """
        Calculate personality fit using cosine similarity
        """
        if np.linalg.norm(student_personality) == 0 or np.linalg.norm(career_personality_fit) == 0:
            return 0.5  # Neutral fit if no personality data
        
        similarity = cosine_similarity([student_personality], [career_personality_fit])[0][0]
        return (similarity + 1) / 2  # Convert from [-1, 1] to [0, 1]
    
    def get_career_recommendations(self, student, top_k=10):
        """
        Get top career recommendations for a student
        """
        from app import db
        
        careers = Career.query.all()
        recommendations = []
        
        for career in careers:
            match_score = self.calculate_match_score(student, career)
            recommendations.append({
                'career': career,
                'match_score': match_score,
                'match_percentage': int(match_score * 100)
            })
        
        # Sort by match score descending
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:top_k]
    
    def get_explanation(self, student, career):
        """
        Generate explanation for why a career was recommended
        """
        reasons = []
        
        # Check skill alignment
        student_skills = [
            ('Technical', student.technical_skills, career.technical_weight),
            ('Communication', student.communication_skills, career.communication_weight),
            ('Analytical', student.analytical_skills, career.analytical_weight),
            ('Creative', student.creative_skills, career.creative_weight),
            ('Leadership', student.leadership_skills, career.leadership_weight)
        ]
        
        for skill_name, student_level, career_requirement in student_skills:
            if career_requirement > 0.5 and student_level >= 3:
                reasons.append(f"Strong {skill_name.lower()} skills match career requirements")
        
        # Check interest alignment
        student_interests = [
            ('Technology', student.interest_technology, career.technology_alignment),
            ('Arts', student.interest_arts, career.arts_alignment),
            ('Business', student.interest_business, career.business_alignment),
            ('Healthcare', student.interest_healthcare, career.healthcare_alignment),
            ('Education', student.interest_education, career.education_alignment),
            ('Agriculture', student.interest_agriculture, career.agriculture_alignment),
            ('Government', student.interest_government, career.government_alignment)
        ]
        
        for interest_name, student_level, career_alignment in student_interests:
            if career_alignment > 0.5 and student_level >= 4:
                reasons.append(f"High interest in {interest_name.lower()} aligns well with this career")
        
        # Rural opportunities
        if career.rural_opportunities:
            reasons.append("Good opportunities available in rural areas")
        
        return reasons if reasons else ["General compatibility based on overall profile"]