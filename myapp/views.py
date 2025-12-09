from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .helpers import (
    extract_resume_text, extract_skills, calculate_resume_score,
    get_missing_skills, recommend_jobs, extract_job_title
)

def upload_resume(request):
    """Handle resume upload"""
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        
        # Validate file type
        if not (resume_file.name.endswith('.pdf') or resume_file.name.endswith('.docx')):
            return render(request, 'upload.html', {'error': 'Only PDF and DOCX files are supported'})
        
        # Save file
        file_path = default_storage.save(f'resumes/{resume_file.name}', resume_file)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        # Extract text
        resume_text = extract_resume_text(full_path)
        
        if resume_text.startswith('Error'):
            return render(request, 'upload.html', {'error': resume_text})
        
        # Extract skills and job titles
        skills = extract_skills(resume_text)
        job_titles = extract_job_title(resume_text)
        score = calculate_resume_score(skills)
        missing_skills = get_missing_skills(skills)
        
        # Store in session
        request.session['resume_text'] = resume_text
        request.session['skills'] = skills
        request.session['job_titles'] = job_titles
        request.session['score'] = score
        request.session['missing_skills'] = missing_skills
        request.session['file_path'] = file_path
        
        return redirect('analysis')
    
    return render(request, 'upload.html')

def analysis(request):
    """Display resume analysis"""
    skills = request.session.get('skills', [])
    job_titles = request.session.get('job_titles', [])
    score = request.session.get('score', 0)
    missing_skills = request.session.get('missing_skills', [])
    
    if not skills:
        return redirect('upload_resume')
    
    context = {
        'skills': skills,
        'job_titles': job_titles,
        'score': score,
        'missing_skills': missing_skills,
        'skill_count': len(skills),
    }
    
    return render(request, 'analysis.html', context)

def jobs(request):
    """Display recommended jobs"""
    skills = request.session.get('skills', [])
    job_titles = request.session.get('job_titles', [])
    
    if not skills:
        return redirect('upload_resume')
    
    recommended_jobs = recommend_jobs(skills, job_titles)
    
    context = {
        'jobs': recommended_jobs,
        'resume_skills': skills,
        'resume_titles': job_titles,
    }
    
    return render(request, 'jobs.html', context)
