import fitz
from docx import Document
import requests
import re

SKILL_LIST = [
    'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift',
    'Kotlin', 'TypeScript', 'SQL', 'HTML', 'CSS', 'React', 'Vue', 'Angular', 'Django',
    'Flask', 'FastAPI', 'Node.js', 'Express', 'Spring', 'ASP.NET', 'Laravel', 'Rails',
    'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Jenkins', 'CI/CD', 'REST API',
    'GraphQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch', 'Machine Learning',
    'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Data Analysis', 'Tableau',
    'Power BI', 'Excel', 'Agile', 'Scrum', 'Linux', 'Windows', 'MacOS', 'Figma', 'Adobe XD',
    'Photoshop', 'Illustrator', 'Blender', 'Unity', 'Unreal Engine', 'Salesforce', 'SAP',
    'Oracle', 'Jira', 'Confluence', 'Slack', 'Communication', 'Leadership', 'Problem Solving',
    'Project Management', 'Business Analysis', 'Quality Assurance', 'Testing', 'Debugging'
]

JOB_TITLES = [
    'Software Engineer', 'Software Developer', 'Full Stack Developer', 'Frontend Developer',
    'Backend Developer', 'Web Developer', 'Mobile Developer', 'iOS Developer', 'Android Developer',
    'DevOps Engineer', 'Cloud Engineer', 'Data Engineer', 'Data Scientist', 'Machine Learning Engineer',
    'AI Engineer', 'QA Engineer', 'Quality Assurance', 'Test Engineer', 'Systems Engineer',
    'Network Engineer', 'Security Engineer', 'Cybersecurity Analyst', 'Database Administrator',
    'System Administrator', 'IT Support', 'Technical Support', 'Solutions Architect',
    'Enterprise Architect', 'Product Manager', 'Project Manager', 'Scrum Master',
    'Business Analyst', 'UX Designer', 'UI Designer', 'Graphic Designer', 'Web Designer',
    'Technical Writer', 'DevOps', 'Site Reliability Engineer', 'SRE', 'Platform Engineer',
    'Infrastructure Engineer', 'Release Engineer', 'Build Engineer', 'Automation Engineer',
    'Performance Engineer', 'Security Analyst', 'Penetration Tester', 'Compliance Officer',
    'Solutions Engineer', 'Technical Consultant', 'IT Consultant', 'Systems Analyst'
]

def extract_text_from_pdf(file_path):
    """Extract text from PDF file using PyMuPDF"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from DOCX file using python-docx"""
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"

def extract_resume_text(file_path):
    """Extract text from resume based on file type"""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"

def extract_skills(resume_text):
    """Extract skills from resume text by matching against SKILL_LIST"""
    found_skills = []
    text_lower = resume_text.lower()
    
    for skill in SKILL_LIST:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            if skill not in found_skills:
                found_skills.append(skill)
    
    return found_skills

def calculate_resume_score(skills_found, total_skills=len(SKILL_LIST)):
    """Calculate resume score based on skills found"""
    if total_skills == 0:
        return 0
    score = (len(skills_found) / total_skills) * 100
    return round(score, 2)

def get_missing_skills(skills_found):
    """Get list of missing skills from the skill list"""
    missing = [skill for skill in SKILL_LIST if skill not in skills_found]
    return missing[:10]  # Return top 10 missing skills

def fetch_jobs_from_api():
    """Fetch job listings from the dummy API"""
    try:
        response = requests.get('https://jsonfakery.com/jobs', timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Error fetching jobs: {str(e)}")
        return []

def extract_job_skills(job_description):
    """Extract skills from job description"""
    job_skills = []
    description_lower = job_description.lower()
    
    for skill in SKILL_LIST:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', description_lower):
            if skill not in job_skills:
                job_skills.append(skill)
    
    return job_skills

def calculate_match_score(resume_skills, job_skills):
    """Calculate match score between resume and job"""
    overlapping = set(resume_skills) & set(job_skills)
    return len(overlapping)

def extract_job_title(resume_text):
    """Extract job title/role from resume text"""
    text_lower = resume_text.lower()
    found_titles = []
    
    for title in JOB_TITLES:
        if re.search(r'\b' + re.escape(title.lower()) + r'\b', text_lower):
            if title not in found_titles:
                found_titles.append(title)
    
    return found_titles

def filter_jobs_by_title(jobs_list, resume_titles):
    """Filter jobs that match resume job titles"""
    if not resume_titles:
        return jobs_list
    
    filtered = []
    resume_titles_lower = [t.lower() for t in resume_titles]
    
    for job in jobs_list:
        if isinstance(job, dict):
            job_title = job.get('title', '').lower()
            
            # Check if job title matches any resume title
            for resume_title in resume_titles_lower:
                if resume_title in job_title or job_title in resume_title:
                    filtered.append(job)
                    break
    
    return filtered

def recommend_jobs(resume_skills, resume_titles=None):
    """Fetch jobs and recommend based on skill match and job title"""
    jobs = fetch_jobs_from_api()
    
    if not jobs:
        return []
    
    # Handle both list and dict responses
    if isinstance(jobs, dict):
        jobs_list = jobs.get('data', []) or jobs.get('jobs', []) or list(jobs.values())
    else:
        jobs_list = jobs
    
    # Filter by job title if available
    if resume_titles:
        jobs_list = filter_jobs_by_title(jobs_list, resume_titles)
    
    recommended = []
    
    for job in jobs_list:
        if isinstance(job, dict):
            job_description = f"{job.get('title', '')} {job.get('description', '')} {job.get('requirements', '')}"
            job_skills = extract_job_skills(job_description)
            match_score = calculate_match_score(resume_skills, job_skills)
            
            job['match_score'] = match_score
            job['matched_skills'] = list(set(resume_skills) & set(job_skills))
            recommended.append(job)
    
    # Sort by match score in descending order
    recommended.sort(key=lambda x: x['match_score'], reverse=True)
    
    return recommended
