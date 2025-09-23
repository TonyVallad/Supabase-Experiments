# main_exercice.py
from supabase import create_client
from dotenv import load_dotenv
import os

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
        print(f"✅ AI Project '{name}' created successfully!")
        return result.data
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        return None

def list_projects():
    """
    Retrieve all AI projects and display them
    """
    try:
        result = supabase.table("ai_projects").select("id, name, model_type, hyperparameters, created_at").execute()
        projects = result.data
        
        print("\n📊 AI Projects List:")
        print("=" * 50)
        
        if not projects:
            print("No projects found.")
            return []
            
        for project in projects:
            print(f"Name: {project['name']} | Type: {project['model_type']}")
            
        print("-" * 50)
        print(f"Total number of projects: {len(projects)}")
        
        return projects
        
    except Exception as e:
        print(f"❌ Error retrieving projects: {e}")
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
        print(f"✅ Dataset '{name}' created successfully!")
        return result.data
    except Exception as e:
        print(f"❌ Error creating dataset: {e}")
        return None

def list_datasets_by_project(ai_project_id: str):
    """
    List all datasets for a specific project
    """
    try:
        result = supabase.table("datasets").select("*").eq("ai_project_id", ai_project_id).execute()
        return result.data
    except Exception as e:
        print(f"❌ Error retrieving datasets: {e}")
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
            
        print("\n📊 Dataset Statistics:")
        print("=" * 60)
        
        total_size = 0
        datasets_by_format = {}
        
        for dataset in datasets:
            total_size += dataset['size_mb']
            format_ds = dataset['format']
            datasets_by_format[format_ds] = datasets_by_format.get(format_ds, 0) + 1
            
            project_name = dataset['ai_projects']['name'] if dataset['ai_projects'] else "Deleted project"
            print(f"• {dataset['name']} ({dataset['size_mb']} MB) - Format: {dataset['format']}")
            print(f"  ↳ Project: {project_name}")
            
        print("-" * 60)
        print(f"📈 Total dataset size: {total_size} MB ({total_size/1024:.1f} GB)")
        print(f"📁 Total number of datasets: {len(datasets)}")
        print(f"📄 Formats used: {', '.join(datasets_by_format.keys())}")
        
        return datasets
        
    except Exception as e:
        print(f"❌ Error calculating statistics: {e}")
        return []

def main():
    print("🚀 Starting Supabase + Python Application")
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
    print("\n📝 Creating AI projects...")
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
        print("\n🎁 BONUS: Dataset Management")
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
        print("\n📋 Creating datasets...")
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
        print("\n⚠️  No projects found, unable to create datasets.")

if __name__ == "__main__":
    main()