#!/usr/bin/env python3
"""
Quick Admin Creation Script - creates default admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import create_admin_user

def main():
    """Create a default admin user"""
    print("🛡️ Creating Admin User...")
    print("=" * 50)
    
    if create_admin_user('admin', 'admin123'):
        print("\n✅ Admin Setup Complete!")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n📋 Next steps:")
        print("   1. Start the app: python app.py")
        print("   2. Go to: http://localhost:5000/admin/login")
        print("   3. Login with admin / admin123")
        print("   4. Review and approve activities!")
    else:
        print("❌ Failed to create admin user")

if __name__ == "__main__":
    main()
