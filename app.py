# app.py
"""
Flask web application for Supabase-Experiments
Provides web interface for AI projects and datasets with GitHub authentication
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from supabase import create_client
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from functools import wraps
from config import ANSI

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
app_secret = os.getenv("FLASK_SECRET_KEY", "your-secret-key-change-this")

app = Flask(__name__)
app.secret_key = app_secret
supabase = create_client(url, key)

def login_required(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Dashboard - Home page with statistics"""
    try:
        if 'user' in session:
            # Get statistics for logged-in users
            projects_result = supabase.table("ai_projects").select("*").execute()
            datasets_result = supabase.table("datasets").select("*").execute()
            
            projects = projects_result.data if projects_result.data else []
            datasets = datasets_result.data if datasets_result.data else []
            
            # Calculate statistics
            total_projects = len(projects)
            total_datasets = len(datasets)
            total_size_mb = sum(d.get('size_mb', 0) for d in datasets)
            
            # Get project types
            project_types = {}
            for project in projects:
                ptype = project.get('model_type', 'Unknown')
                project_types[ptype] = project_types.get(ptype, 0) + 1
            
            # Get dataset formats
            dataset_formats = {}
            for dataset in datasets:
                fmt = dataset.get('format', 'Unknown')
                dataset_formats[fmt] = dataset_formats.get(fmt, 0) + 1
            
            stats = {
                'total_projects': total_projects,
                'total_datasets': total_datasets,
                'total_size_mb': total_size_mb,
                'total_size_gb': round(total_size_mb / 1024, 1),
                'project_types': project_types,
                'dataset_formats': dataset_formats,
                'recent_projects': projects[-5:] if projects else []
            }
            
            return render_template('index.html', stats=stats, user=session['user'])
        else:
            return render_template('index.html', stats=None, user=None)
            
    except Exception as e:
        print(f"{ANSI['R']}Error loading dashboard: {e}{ANSI['W']}")
        flash('Error loading dashboard data.', 'error')
        return render_template('index.html', stats=None, user=session.get('user'))

@app.route('/login')
def login():
    """Login page"""
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/auth/github')
def github_auth():
    """Initiate GitHub OAuth flow using Supabase Auth"""
    try:
        # Use Supabase's built-in OAuth sign-in
        response = supabase.auth.sign_in_with_oauth({
            "provider": "github",
            "options": {
                "redirect_to": f"{request.url_root}auth/callback"
            }
        })
        
        # Redirect to Supabase's OAuth URL
        return redirect(response.url)
        
    except Exception as e:
        print(f"{ANSI['R']}GitHub auth error: {e}{ANSI['W']}")
        flash('Error initiating GitHub authentication.', 'error')
        return redirect(url_for('login'))

@app.route('/auth/callback')
def auth_callback():
    """Handle OAuth callback from Supabase"""
    # This page will handle the OAuth callback and trigger the JavaScript auth flow
    return render_template('auth_callback.html')

@app.route('/auth/signin', methods=['POST'])
def handle_auth_signin():
    """Handle authentication from frontend JavaScript"""
    try:
        data = request.get_json()
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        user_data = data.get('user')
        
        if access_token and user_data:
            # Store user info in Flask session
            session['user'] = {
                'id': user_data.get('id'),
                'email': user_data.get('email'),
                'name': user_data.get('user_metadata', {}).get('full_name') or user_data.get('user_metadata', {}).get('name', 'User'),
                'avatar_url': user_data.get('user_metadata', {}).get('avatar_url', ''),
                'username': user_data.get('user_metadata', {}).get('user_name', ''),
            }
            session['access_token'] = access_token
            if refresh_token:
                session['refresh_token'] = refresh_token
            
            return jsonify({'success': True, 'redirect': url_for('index')})
        
        return jsonify({'success': False, 'error': 'Invalid authentication data'})
        
    except Exception as e:
        print(f"{ANSI['R']}Auth signin error: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/logout')
def logout():
    """Logout user"""
    try:
        if 'access_token' in session:
            # Sign out from Supabase
            supabase.auth.sign_out()
        
        # Clear Flask session
        session.clear()
        flash('You have been logged out.', 'info')
        
    except Exception as e:
        print(f"{ANSI['R']}Logout error: {e}{ANSI['W']}")
        # Clear session anyway
        session.clear()
    
    return redirect(url_for('index'))

@app.route('/projects')
@login_required
def projects():
    """AI Projects listing page"""
    try:
        result = supabase.table("ai_projects").select("*").order("created_at", desc=True).execute()
        projects_list = result.data if result.data else []
        return render_template('projects.html', projects=projects_list, user=session['user'])
    except Exception as e:
        print(f"{ANSI['R']}Error loading projects: {e}{ANSI['W']}")
        flash('Error loading projects.', 'error')
        return render_template('projects.html', projects=[], user=session['user'])

@app.route('/datasets')
@login_required
def datasets():
    """Datasets listing page"""
    try:
        # Get datasets with project information
        result = supabase.table("datasets").select("""
            id, name, description, size_mb, format, source_url, created_at,
            ai_projects(id, name, model_type)
        """).order("created_at", desc=True).execute()
        
        datasets_list = result.data if result.data else []
        
        # Also get all projects for the create form
        projects_result = supabase.table("ai_projects").select("id, name").execute()
        projects_list = projects_result.data if projects_result.data else []
        
        return render_template('datasets.html', 
                             datasets=datasets_list, 
                             projects=projects_list, 
                             user=session['user'])
    except Exception as e:
        print(f"{ANSI['R']}Error loading datasets: {e}{ANSI['W']}")
        flash('Error loading datasets.', 'error')
        return render_template('datasets.html', datasets=[], projects=[], user=session['user'])

@app.route('/project/<project_id>')
@login_required
def project_detail(project_id):
    """Individual project detail page"""
    try:
        # Get project details
        project_result = supabase.table("ai_projects").select("*").eq("id", project_id).execute()
        if not project_result.data:
            flash('Project not found.', 'error')
            return redirect(url_for('projects'))
        
        project = project_result.data[0]
        
        # Get associated datasets
        datasets_result = supabase.table("datasets").select("*").eq("ai_project_id", project_id).execute()
        datasets_list = datasets_result.data if datasets_result.data else []
        
        return render_template('project_detail.html', 
                             project=project, 
                             datasets=datasets_list, 
                             user=session['user'])
    except Exception as e:
        print(f"{ANSI['R']}Error loading project detail: {e}{ANSI['W']}")
        flash('Error loading project details.', 'error')
        return redirect(url_for('projects'))

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/config', methods=['GET'])
def api_get_config():
    """API: Get public configuration for frontend"""
    return jsonify({
        'success': True,
        'supabase_url': url,
        'supabase_key': key  # This is the anon/public key, safe to expose
    })

@app.route('/api/projects', methods=['GET'])
@login_required
def api_get_projects():
    """API: Get all projects with optional pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit
        
        # Get total count
        count_result = supabase.table("ai_projects").select("id", count="exact").execute()
        total = len(count_result.data) if count_result.data else 0
        
        # Get paginated projects
        result = supabase.table("ai_projects").select("*").order("created_at", desc=True).range(offset, offset + limit - 1).execute()
        projects = result.data if result.data else []
        
        return jsonify({
            'success': True,
            'data': projects,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
    except Exception as e:
        print(f"{ANSI['R']}API Error getting projects: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
@login_required
def api_create_project():
    """API: Create new project"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('model_type'):
            return jsonify({'success': False, 'error': 'Name and model_type are required'}), 400
        
        result = supabase.table("ai_projects").insert({
            "name": data['name'],
            "description": data.get('description', ''),
            "model_type": data['model_type'],
            "hyperparameters": data.get('hyperparameters', {})
        }).execute()
        
        return jsonify({'success': True, 'data': result.data[0] if result.data else None})
    except Exception as e:
        print(f"{ANSI['R']}API Error creating project: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['GET'])
@login_required
def api_get_project(project_id):
    """API: Get specific project"""
    try:
        result = supabase.table("ai_projects").select("*").eq("id", project_id).execute()
        if not result.data:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        print(f"{ANSI['R']}API Error getting project: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['PUT'])
@login_required
def api_update_project(project_id):
    """API: Update specific project"""
    try:
        data = request.get_json()
        
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'model_type' in data:
            update_data['model_type'] = data['model_type']
        if 'hyperparameters' in data:
            update_data['hyperparameters'] = data['hyperparameters']
        
        result = supabase.table("ai_projects").update(update_data).eq("id", project_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        print(f"{ANSI['R']}API Error updating project: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['DELETE'])
@login_required
def api_delete_project(project_id):
    """API: Delete specific project"""
    try:
        result = supabase.table("ai_projects").delete().eq("id", project_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        return jsonify({'success': True, 'message': 'Project deleted successfully'})
    except Exception as e:
        print(f"{ANSI['R']}API Error deleting project: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/datasets', methods=['GET'])
@login_required
def api_get_datasets():
    """API: Get all datasets with optional pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit
        
        # Get total count
        count_result = supabase.table("datasets").select("id", count="exact").execute()
        total = len(count_result.data) if count_result.data else 0
        
        # Get paginated datasets with project info
        result = supabase.table("datasets").select("""
            id, name, description, size_mb, format, source_url, created_at,
            ai_projects(id, name, model_type)
        """).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
        
        datasets = result.data if result.data else []
        
        return jsonify({
            'success': True,
            'data': datasets,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
    except Exception as e:
        print(f"{ANSI['R']}API Error getting datasets: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/datasets', methods=['POST'])
@login_required
def api_create_dataset():
    """API: Create new dataset"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('size_mb') or not data.get('ai_project_id'):
            return jsonify({'success': False, 'error': 'Name, size_mb, and ai_project_id are required'}), 400
        
        result = supabase.table("datasets").insert({
            "name": data['name'],
            "description": data.get('description', ''),
            "size_mb": int(data['size_mb']),
            "format": data.get('format', ''),
            "source_url": data.get('source_url', ''),
            "ai_project_id": data['ai_project_id']
        }).execute()
        
        return jsonify({'success': True, 'data': result.data[0] if result.data else None})
    except Exception as e:
        print(f"{ANSI['R']}API Error creating dataset: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/datasets/<dataset_id>', methods=['GET'])
@login_required
def api_get_dataset(dataset_id):
    """API: Get specific dataset"""
    try:
        result = supabase.table("datasets").select("""
            id, name, description, size_mb, format, source_url, created_at,
            ai_projects(id, name, model_type)
        """).eq("id", dataset_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404
        
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        print(f"{ANSI['R']}API Error getting dataset: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/datasets/<dataset_id>', methods=['PUT'])
@login_required
def api_update_dataset(dataset_id):
    """API: Update specific dataset"""
    try:
        data = request.get_json()
        
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'size_mb' in data:
            update_data['size_mb'] = int(data['size_mb'])
        if 'format' in data:
            update_data['format'] = data['format']
        if 'source_url' in data:
            update_data['source_url'] = data['source_url']
        if 'ai_project_id' in data:
            update_data['ai_project_id'] = data['ai_project_id']
        
        result = supabase.table("datasets").update(update_data).eq("id", dataset_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404
        
        return jsonify({'success': True, 'data': result.data[0]})
    except Exception as e:
        print(f"{ANSI['R']}API Error updating dataset: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/datasets/<dataset_id>', methods=['DELETE'])
@login_required
def api_delete_dataset(dataset_id):
    """API: Delete specific dataset"""
    try:
        result = supabase.table("datasets").delete().eq("id", dataset_id).execute()
        
        if not result.data:
            return jsonify({'success': False, 'error': 'Dataset not found'}), 404
        
        return jsonify({'success': True, 'message': 'Dataset deleted successfully'})
    except Exception as e:
        print(f"{ANSI['R']}API Error deleting dataset: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>/datasets', methods=['GET'])
@login_required
def api_get_project_datasets(project_id):
    """API: Get datasets for specific project"""
    try:
        result = supabase.table("datasets").select("*").eq("ai_project_id", project_id).order("created_at", desc=True).execute()
        datasets = result.data if result.data else []
        
        return jsonify({'success': True, 'data': datasets})
    except Exception as e:
        print(f"{ANSI['R']}API Error getting project datasets: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
@login_required
def api_get_stats():
    """API: Get dashboard statistics"""
    try:
        # Get projects
        projects_result = supabase.table("ai_projects").select("*").execute()
        projects = projects_result.data if projects_result.data else []
        
        # Get datasets
        datasets_result = supabase.table("datasets").select("*").execute()
        datasets = datasets_result.data if datasets_result.data else []
        
        # Calculate statistics
        total_projects = len(projects)
        total_datasets = len(datasets)
        total_size_mb = sum(d.get('size_mb', 0) for d in datasets)
        
        # Project types breakdown
        project_types = {}
        for project in projects:
            ptype = project.get('model_type', 'Unknown')
            project_types[ptype] = project_types.get(ptype, 0) + 1
        
        # Dataset formats breakdown
        dataset_formats = {}
        for dataset in datasets:
            fmt = dataset.get('format', 'Unknown')
            dataset_formats[fmt] = dataset_formats.get(fmt, 0) + 1
        
        stats = {
            'total_projects': total_projects,
            'total_datasets': total_datasets,
            'total_size_mb': total_size_mb,
            'total_size_gb': round(total_size_mb / 1024, 1),
            'project_types': project_types,
            'dataset_formats': dataset_formats
        }
        
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        print(f"{ANSI['R']}API Error getting stats: {e}{ANSI['W']}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print(f"🌐 {ANSI['G']}Starting Supabase-Experiments Web Application{ANSI['W']}")
    print(f"{ANSI['B']}Visit: http://localhost:5000{ANSI['W']}")
    app.run(debug=True, host='0.0.0.0', port=5000)