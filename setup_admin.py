#!/usr/bin/env python3
"""
Admin Setup Script for Eco-Friendly Reward App

This script creates an admin user for the application.
Run this script to set up admin access for the review dashboard.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import create_admin_user

def main():
    print("🛡️ Eco-Friendly Reward App - Admin Setup")
    print("=" * 50)

    # Get admin credentials
    username = input("Enter admin username: ").strip()
    if not username:
        print("❌ Username cannot be empty.")
        return

    password = input("Enter admin password: ").strip()
    if not password:
        print("❌ Password cannot be empty.")
        return

    confirm_password = input("Confirm admin password: ").strip()
    if password != confirm_password:
        print("❌ Passwords do not match.")
        return

    # Create admin user
    print("\n🔄 Creating admin user...")
    if create_admin_user(username, password):
        print("✅ Admin user created successfully!")
        print(f"   Username: {username}")
        print("\n📋 Next steps:")
        print("   1. Start the app: python app.py")
        print("   2. Go to: http://localhost:5000/admin/login")
        print("   3. Login with your admin credentials")
        print("   4. Access the review dashboard to approve activities")
    else:
        print("❌ Failed to create admin user. Check the error messages above.")

if __name__ == "__main__":
    main()