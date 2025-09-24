# clear_database.py
"""
Script to clear all data from Supabase database tables.
This script will delete all records from ai_projects and datasets tables.
"""

from supabase import create_client
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ANSI

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

def confirm_deletion():
    """
    Ask user for confirmation before proceeding with deletion
    """
    print(f"{ANSI['Y']}⚠️  WARNING: This will delete ALL data from your database tables!{ANSI['W']}")
    print(f"{ANSI['Y']}This action cannot be undone.{ANSI['W']}")
    
    response = input(f"\n{ANSI['B']}Do you want to continue? (type 'yes' to confirm): {ANSI['W']}")
    return response.lower() == 'yes'

def clear_datasets_table():
    """
    Clear all records from the datasets table
    """
    try:
        print(f"\n{ANSI['Y']}🗑️  Clearing datasets table...{ANSI['W']}")
        
        # Get count before deletion
        count_result = supabase.table("datasets").select("id", count="exact").execute()
        initial_count = len(count_result.data) if count_result.data else 0
        
        if initial_count == 0:
            print(f"{ANSI['B']}📝 Datasets table is already empty.{ANSI['W']}")
            return True
            
        # Delete all records
        result = supabase.table("datasets").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        
        print(f"{ANSI['G']}✅ Successfully deleted {initial_count} records from datasets table.{ANSI['W']}")
        return True
        
    except Exception as e:
        print(f"{ANSI['R']}❌ Error clearing datasets table: {e}{ANSI['W']}")
        return False

def clear_ai_projects_table():
    """
    Clear all records from the ai_projects table
    """
    try:
        print(f"\n{ANSI['Y']}🗑️  Clearing ai_projects table...{ANSI['W']}")
        
        # Get count before deletion
        count_result = supabase.table("ai_projects").select("id", count="exact").execute()
        initial_count = len(count_result.data) if count_result.data else 0
        
        if initial_count == 0:
            print(f"{ANSI['B']}📝 AI Projects table is already empty.{ANSI['W']}")
            return True
            
        # Delete all records
        result = supabase.table("ai_projects").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        
        print(f"{ANSI['G']}✅ Successfully deleted {initial_count} records from ai_projects table.{ANSI['W']}")
        return True
        
    except Exception as e:
        print(f"{ANSI['R']}❌ Error clearing ai_projects table: {e}{ANSI['W']}")
        return False

def get_table_stats():
    """
    Get current statistics of tables before clearing
    """
    try:
        print(f"\n{ANSI['B']}📊 Current Database Statistics:{ANSI['W']}")
        print("=" * 40)
        
        # Count AI projects
        projects_result = supabase.table("ai_projects").select("id", count="exact").execute()
        projects_count = len(projects_result.data) if projects_result.data else 0
        
        # Count datasets
        datasets_result = supabase.table("datasets").select("id", count="exact").execute()
        datasets_count = len(datasets_result.data) if datasets_result.data else 0
        
        print(f"• AI Projects: {projects_count} records")
        print(f"• Datasets: {datasets_count} records")
        print("-" * 40)
        print(f"Total records: {projects_count + datasets_count}")
        
        return projects_count + datasets_count > 0
        
    except Exception as e:
        print(f"{ANSI['R']}❌ Error getting table statistics: {e}{ANSI['W']}")
        return False

def main():
    print(f"🧹 {ANSI['G']}Database Cleanup Script{ANSI['W']}")
    print("=" * 50)
    
    # Show current stats
    has_data = get_table_stats()
    
    if not has_data:
        print(f"\n{ANSI['B']}✨ Database is already empty. Nothing to clear!{ANSI['W']}")
        return
    
    # Ask for confirmation
    if not confirm_deletion():
        print(f"\n{ANSI['Y']}🚫 Operation cancelled by user.{ANSI['W']}")
        return
    
    print(f"\n{ANSI['G']}🚀 Starting database cleanup...{ANSI['W']}")
    
    # Clear datasets first (due to foreign key constraints)
    datasets_success = clear_datasets_table()
    
    # Clear AI projects
    projects_success = clear_ai_projects_table()
    
    # Final summary
    print(f"\n{ANSI['G']}📋 Cleanup Summary:{ANSI['W']}")
    print("=" * 30)
    
    if datasets_success and projects_success:
        print(f"{ANSI['G']}✅ All tables cleared successfully!{ANSI['W']}")
        print(f"{ANSI['B']}🎉 Database is now empty and ready for fresh data.{ANSI['W']}")
    else:
        print(f"{ANSI['R']}⚠️  Some operations failed. Check the errors above.{ANSI['W']}")
    
    # Show final stats
    get_table_stats()

if __name__ == "__main__":
    main()
