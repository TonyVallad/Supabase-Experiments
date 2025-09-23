-- SQL Script to create the datasets table (bonus part)
-- Execute in the Supabase Table Editor

CREATE TABLE datasets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  size_mb INTEGER NOT NULL, -- Size in megabytes
  format VARCHAR(50), -- CSV, JSON, PARQUET, etc.
  source_url TEXT,
  ai_project_id UUID REFERENCES ai_projects(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index to optimize searches by project
CREATE INDEX idx_datasets_ai_project_id ON datasets(ai_project_id);

-- Example insertions (optional)
-- INSERT INTO datasets (name, description, size_mb, format, ai_project_id) 
-- VALUES ('Spam emails dataset', 'Collection of labeled spam/non-spam emails', 150, 'CSV', 'PROJECT_UUID');