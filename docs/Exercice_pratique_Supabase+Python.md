# Practical Exercise – Supabase + Python

## Objective
Create a mini Python application connected to Supabase to manage an AI project:

- Insert an AI project into the database,
- Read existing projects,
- Display a simple summary in console.

This exercise allows you to manipulate Supabase from Python and understand the benefits of CRUD (Create/Read) and JSONB hyperparameters.

## What is JSONB?

- **JSON**: text format to represent objects (key-value pairs, lists, etc.).
- **JSONB**: this is an optimized binary version of JSON in PostgreSQL.  
  - The "B" stands for Binary.  
  - Data is stored in an internal compressed format → more efficient for search and queries.  

👉 In other words: JSONB = NoSQL flexibility (semi-structured data storage) in a relational SQL database.

## Estimated Duration

- 20 minutes → simple version (project CRUD).
- 30 minutes → with the datasets bonus.

---

## What you need to do

### Step 1: Configuration

1. Create a new project in Supabase.
2. In the **Table Editor**, execute this SQL to prepare your database:

```sql
CREATE TABLE ai_projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  model_type VARCHAR(100), -- NLP, Computer Vision, etc.
  hyperparameters JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

3. Get your API keys in **Project Settings > API**:
   - Project URL  
   - anon key  

4. In your Python project, create a `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

---

### Step 2: Installation

Create a **venv**, install minimal dependencies:

```bash
pip install supabase python-dotenv
```

---

### Step 3: Starter Code

A skeleton is provided (`main_exercice.py`). You need to complete the functions.

```python
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
    TODO: Insert an AI project into the ai_projects table
    """
    pass

def list_projects():
    """
    TODO: Retrieve all AI projects and display them
    """
    pass

def main():
    # TODO: Call create_ai_project with your own values
    # TODO: Call list_projects to verify
    pass

if __name__ == "__main__":
    main()
```

---

### Step 4: Your Mission

1. Complete `create_ai_project` to insert an AI project with your own values:  
   - `name` = free choice (ex: "Spam Detection")  
   - `description` = 1 sentence  
   - `model_type` = your choice (NLP, Computer Vision, …)  
   - `hyperparameters` = JSON dictionary (ex: `{"epochs": 10, "lr": 0.001}`)  

2. Complete `list_projects` to:  
   - retrieve all projects from the table,  
   - display in console the name, model_type and total number of projects.  

---

## Bonus (optional)

- Add a `datasets` table linked to AI projects.  
- Create a dataset, link it to a project and display the total size of datasets.

---

## Expected Result (console example)

```
Name: Spam Detection | Type: NLP
Total number of projects: 1
```