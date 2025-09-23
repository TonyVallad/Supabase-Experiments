#!/usr/bin/env python3
"""
Setup script for Supabase + Python Exercise
English version with AI projects and datasets management
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Check .env file and provide guidance"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
        
    print("❌ .env file not found")
    print("💡 Create a .env file with your Supabase credentials:")
    print("   SUPABASE_URL=https://your-project.supabase.co")
    print("   SUPABASE_KEY=your-public-anon-key")

def check_dependencies():
    """Check if required packages are installed"""
    packages_to_check = [
        ('supabase', 'supabase'),
        ('python-dotenv', 'dotenv')  # package name vs import name
    ]
    missing_packages = []
    
    for package_name, import_name in packages_to_check:
        try:
            __import__(import_name)
            print(f"✅ {package_name}: OK")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name}: Missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print(f"💡 Install with: pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All required packages are installed")
        return True

def show_available_files():
    """Show available exercise files"""
    print("\n📁 Project files:")
    
    files = [
        ("Main Application", "main_exercice.py"),
        ("Database Schema", "datasets_table.sql"),
        ("Documentation", "docs/Exercice_pratique_Supabase+Python.md"),
        ("README", "README.md")
    ]
    
    for description, file_path in files:
        file_exists = Path(file_path).exists()
        status = "✅" if file_exists else "❌"
        print(f"{status} {description}: {file_path}")

def main():
    print("🚀 Supabase + Python Exercise Setup")
    print("=" * 50)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Show available files
    show_available_files()
    
    if deps_ok:
        print("\n🎯 Quick start:")
        print("1. Create/edit .env file with your Supabase credentials")
        print("2. Execute SQL schema: datasets_table.sql in your Supabase dashboard")
        print("3. Run: python main_exercice.py")
        print("\n📚 Features: AI projects + datasets management with JSONB")
    else:
        print("\n⚠️  Please install missing dependencies first")
        
if __name__ == "__main__":
    main()