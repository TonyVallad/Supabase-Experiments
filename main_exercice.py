# main_exercice.py
from supabase import create_client
from dotenv import load_dotenv
import os
from config import ANSI

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def create_ai_project(name: str, description: str, model_type: str, hyperparameters: dict):
    """
    Insert an AI project into the ai_projects table
    """
    try:
        result = supabase.table("ai_projects").insert({
            "name": name,
            "description": description,
            "model_type": model_type,
            "hyperparameters": hyperparameters
        }).execute()
        print(f"✅ AI Project '{ANSI['G']}{name}{ANSI['W']}' created successfully!")
        return result.data
    except Exception as e:
        print(f"{ANSI['R']}❌ Error creating project: {e}{ANSI['W']}")
        return None

def list_projects():
    """
    Retrieve all AI projects and display them
    """
    try:
        result = supabase.table("ai_projects").select("id, name, model_type, hyperparameters, created_at").execute()
        projects = result.data
        
        print(f"\n📊 {ANSI['G']}AI Projects List:{ANSI['W']}")
        print("=" * 50)
        
        if not projects:
            print("No projects found.")
            return []
            
        for project in projects:
            print(f"{ANSI['B']}Name:{ANSI['W']} {project['name']} | {ANSI['B']}Type:{ANSI['W']} {project['model_type']}")
            
        print("-" * 50)
        print(f"{ANSI['B']}Total number of projects:{ANSI['W']} {len(projects)}")
        
        return projects
        
    except Exception as e:
        print(f"{ANSI['R']}❌ Error retrieving projects: {e}{ANSI['W']}")
        return []

def create_dataset(name: str, description: str, size_mb: int, format: str, ai_project_id: str, source_url: str = None):
    """
    Create a dataset linked to an AI project
    """
    try:
        result = supabase.table("datasets").insert({
            "name": name,
            "description": description,
            "size_mb": size_mb,
            "format": format,
            "source_url": source_url,
            "ai_project_id": ai_project_id
        }).execute()
        print(f"✅ Dataset '{ANSI['G']}{name}{ANSI['W']}' created successfully!")
        return result.data
    except Exception as e:
        print(f"{ANSI['R']}❌ Error creating dataset: {e}{ANSI['W']}")
        return None

def list_datasets_by_project(ai_project_id: str):
    """
    List all datasets for a specific project
    """
    try:
        result = supabase.table("datasets").select("*").eq("ai_project_id", ai_project_id).execute()
        return result.data
    except Exception as e:
        print(f"{ANSI['R']}❌ Error retrieving datasets: {e}{ANSI['W']}")
        return []

def datasets_statistics():
    """
    Display global dataset statistics
    """
    try:
        # Get all datasets with project information
        result = supabase.table("datasets").select("""
            id, name, size_mb, format,
            ai_projects(name, model_type)
        """).execute()
        
        datasets = result.data
        
        if not datasets:
            print("\n📊 No datasets found.")
            return
            
        print(f"\n📊 {ANSI['G']}Dataset Statistics:{ANSI['W']}")
        print("=" * 60)
        
        total_size = 0
        datasets_by_format = {}
        
        for dataset in datasets:
            total_size += dataset['size_mb']
            format_ds = dataset['format']
            datasets_by_format[format_ds] = datasets_by_format.get(format_ds, 0) + 1
            
            project_name = dataset['ai_projects']['name'] if dataset['ai_projects'] else "Deleted project"
            print(f"• {dataset['name']} ({dataset['size_mb']} MB) - {ANSI['B']}Format:{ANSI['W']} {dataset['format']}")
            print(f"  ↳ {ANSI['B']}Project:{ANSI['W']} {project_name}")
            
        print("-" * 60)
        print(f"📈 {ANSI['B']}Total dataset size:{ANSI['W']} {total_size} MB ({total_size/1024:.1f} GB)")
        print(f"📁 {ANSI['B']}Total number of datasets:{ANSI['W']} {len(datasets)}")
        print(f"📄 {ANSI['B']}Formats used:{ANSI['W']} {', '.join(datasets_by_format.keys())}")
        
        return datasets
        
    except Exception as e:
        print(f"{ANSI['R']}❌ Error calculating statistics: {e}{ANSI['W']}")
        return []

def main():
    print(f"🚀 {ANSI['G']}Starting Supabase-Experiments{ANSI['W']}")
    print("=" * 60)
    
    # Create some example AI projects
    example_projects = [
        {
            "name": "Spam Detection",
            "description": "Automatic classification of spam/non-spam emails",
            "model_type": "NLP",
            "hyperparameters": {"epochs": 10, "lr": 0.001, "batch_size": 32}
        },
        {
            "name": "Face Recognition",
            "description": "Person identification from images",
            "model_type": "Computer Vision", 
            "hyperparameters": {"epochs": 50, "lr": 0.0001, "dropout": 0.2, "image_size": 224}
        },
        {
            "name": "Weather Prediction",
            "description": "Weather forecasting based on historical data",
            "model_type": "Time Series",
            "hyperparameters": {"window_size": 7, "hidden_units": 128, "lr": 0.005}
        }
    ]
    
    # Create projects
    print(f"\n📝 {ANSI['Y']}Creating AI projects...{ANSI['W']}")
    for project in example_projects:
        create_ai_project(
            name=project["name"],
            description=project["description"], 
            model_type=project["model_type"],
            hyperparameters=project["hyperparameters"]
        )
    
    # List all projects
    print("\n")
    projects = list_projects()
    
    # BONUS: Datasets demonstration
    if projects and len(projects) > 0:
        print(f"\n🎁 {ANSI['G']}BONUS: Dataset Management{ANSI['W']}")
        print("=" * 60)
        
        # Create some example datasets for the created projects
        example_datasets = [
            {
                "name": "Enron Email Dataset",
                "description": "Email collection for spam/ham classification",
                "size_mb": 450,
                "format": "CSV",
                "source_url": "https://www.cs.cmu.edu/~enron/"
            },
            {
                "name": "ImageNet Faces",
                "description": "Face images for facial recognition", 
                "size_mb": 2048,
                "format": "JPG",
                "source_url": "http://vis-www.cs.umass.edu/lfw/"
            },
            {
                "name": "Historical Weather Data",
                "description": "Historical meteorological data",
                "size_mb": 320,
                "format": "JSON",
                "source_url": "https://openweathermap.org/"
            }
        ]
        
        # Create datasets by linking them to projects
        print(f"\n📋 {ANSI['Y']}Creating datasets...{ANSI['W']}")
        for i, dataset in enumerate(example_datasets):
            if i < len(projects):
                project_id = projects[i]['id'] if 'id' in projects[i] else None
                if project_id:
                    create_dataset(
                        name=dataset["name"],
                        description=dataset["description"],
                        size_mb=dataset["size_mb"],
                        format=dataset["format"],
                        ai_project_id=project_id,
                        source_url=dataset["source_url"]
                    )
        
        # Display dataset statistics
        datasets_statistics()
    else:
        print(f"\n⚠️  {ANSI['R']}No projects found, unable to create datasets.{ANSI['W']}")

if __name__ == "__main__":
    main()