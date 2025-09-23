# Supabase + Python - Complete Practical Exercise

## Description

This project implements a mini Python application connected to Supabase to manage AI projects and their associated datasets.

## Implemented Features

### ✅ Step 4 - Core Functions
- **`create_ai_project()`** : AI project insertion with JSONB hyperparameters
- **`list_projects()`** : Project display with statistics
- **`main()`** : Demonstration with 3 example projects

### 🎁 Bonus - Dataset Management  
- **Table `datasets`** : Linked to AI projects with foreign key constraint
- **`create_dataset()`** : Dataset creation linked to projects
- **`datasets_statistics()`** : Total size calculation and statistics
- **Complete demonstration** : Automatic creation of example datasets

## Project Structure

```
├── main_exercice.py              # Main completed application
├── datasets_table_en.sql         # SQL script to create datasets table
├── .env                          # Environment variables (to create)
└── docs/
    └── Exercice_pratique_Supabase+Python.md
```

## Required Configuration

1. **Create a Supabase project** and execute this SQL:

```sql
-- Main AI projects table
CREATE TABLE ai_projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  model_type VARCHAR(100),
  hyperparameters JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

2. **For the bonus**, also execute the content of `datasets_table_en.sql`

3. **`.env` file** :
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

## Installation and Execution

```bash
# Install dependencies
pip install supabase python-dotenv

# Run the application
python main_exercice.py
```

## Expected Output Example

```
🚀 Starting Supabase + Python Application
============================================================

📝 Creating AI projects...
✅ AI Project 'Spam Detection' created successfully!
✅ AI Project 'Face Recognition' created successfully!
✅ AI Project 'Weather Prediction' created successfully!

📊 AI Projects List:
==================================================
Name: Spam Detection | Type: NLP
Name: Face Recognition | Type: Computer Vision
Name: Weather Prediction | Type: Time Series
--------------------------------------------------
Total number of projects: 3

🎁 BONUS: Dataset Management
============================================================

📋 Creating datasets...
✅ Dataset 'Enron Email Dataset' created successfully!
✅ Dataset 'ImageNet Faces' created successfully!
✅ Dataset 'Historical Weather Data' created successfully!

📊 Dataset Statistics:
============================================================
• Enron Email Dataset (450 MB) - Format: CSV
  ↳ Project: Spam Detection
• ImageNet Faces (2048 MB) - Format: JPG
  ↳ Project: Face Recognition
• Historical Weather Data (320 MB) - Format: JSON
  ↳ Project: Weather Prediction
------------------------------------------------------------
📈 Total dataset size: 2818 MB (2.8 GB)
📁 Total number of datasets: 3
📄 Formats used: CSV, JPG, JSON
```

## Demonstrated Concepts

- ✅ **CRUD Operations** : Create (INSERT), Read (SELECT)
- ✅ **JSONB** : Flexible storage of hyperparameters  
- ✅ **SQL Relations** : Foreign keys between projects and datasets
- ✅ **Error Handling** : Try/catch with user messages
- ✅ **JOIN Queries** : Retrieval of linked data
- ✅ **Aggregation** : Statistical calculations (sum, count)