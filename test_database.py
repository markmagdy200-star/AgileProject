# test_database.py
try:
    from University_Controller import UniversityController
    from database_schema import UniversityDatabase
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all files are in the same directory.")
    exit(1)

def test_database_integration():
    print("Testing Database Integration...")
    
    try:
        # Create controller
        controller = UniversityController()
        
        # Test 1: Check if database was created
        print("\n1. Checking database connection...")
        try:
            if hasattr(controller, 'database') and controller.database:
                cursor = controller.database.conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"   ✅ Found {len(tables)} tables in database")
                
                # List tables
                table_names = [t[0] for t in tables]
                print(f"   Tables: {', '.join(table_names[:5])}...")  # Show first 5
            else:
                print("   ⚠️  Database not available in controller")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Add a new student
        print("\n2. Adding new student to system...")
        try:
            student_data = {
                'student_id': 'TEST001',
                'first_name': 'Test',
                'last_name': 'Student',
                'email': 'test@uni.edu',
                'department': 'Testing',
                'enrollment_year': 2024,
                'gpa': 3.0
            }
            
            result = controller.register_new_student(student_data)
            print(f"   ✅ {result}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Try database queries if available
        print("\n3. Testing database queries...")
        try:
            if hasattr(controller, 'get_student_from_db'):
                student_db = controller.get_student_from_db('TEST001')
                if student_db:
                    print(f"   ✅ Found in DB: {student_db['first_name']} {student_db['last_name']}")
                else:
                    print("   ⚠️  Student not found in database")
            else:
                print("   ⚠️  Database query methods not available")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 4: Try EAV system if available
        print("\n4. Testing EAV system...")
        try:
            if hasattr(controller, 'create_software_license'):
                result = controller.create_software_license('TESTLIC', 'Test License', 10)
                print(f"   ✅ {result}")
                
                # Get licenses
                licenses = controller.database.get_entities_by_type('license')
                print(f"   Total licenses in EAV: {len(licenses)}")
            else:
                print("   ⚠️  EAV methods not available")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Clean up
        print("\n5. Cleaning up...")
        try:
            # Delete test student from filesystem
            if hasattr(controller, 'student_mgr'):
                controller.student_mgr.delete_student('TEST001')
            
            # Delete from database if available
            if hasattr(controller, 'database') and controller.database:
                controller.database.conn.execute("DELETE FROM students WHERE student_id = 'TEST001'")
                controller.database.conn.commit()
            
            # Close database
            if hasattr(controller, 'close_database'):
                controller.close_database()
            
            print("   ✅ Test data cleaned up")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("\n" + "="*50)
        print("✅ Database integration test completed!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Critical error in test: {e}")
        print("Check that all files are in the same directory.")

if __name__ == "__main__":
    test_database_integration()