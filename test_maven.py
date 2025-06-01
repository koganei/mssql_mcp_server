# Test script for Maven wrapper functionality
import sys
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_maven")

# Add parent directory to path so we can import modules
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))
logger.debug(f"Added to sys.path: {str(src_dir)}")
logger.debug(f"Current sys.path: {sys.path}")

# Now imports should work
try:
    logger.debug("Attempting to import from maven_startup_mcp_server.maven_wrapper")
    from maven_startup_mcp_server.maven_wrapper import run_maven, compile, run_tests, find_maven_basedir
    logger.debug("Successfully imported maven_wrapper functions")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.debug("Trying direct import...")
    
    # Try direct import
    sys.path.insert(0, str(current_dir / "src" / "maven_startup_mcp_server"))
    logger.debug(f"Updated sys.path: {sys.path}")
    
    # Try listing files
    wrapper_path = current_dir / "src" / "maven_startup_mcp_server" / "maven_wrapper.py"
    logger.debug(f"Looking for file: {wrapper_path}")
    logger.debug(f"File exists: {wrapper_path.exists()}")
    
    # Try direct import
    try:
        import maven_wrapper
        logger.debug("Successfully imported maven_wrapper directly")
        run_maven = maven_wrapper.run_maven
        compile = maven_wrapper.compile
        run_tests = maven_wrapper.run_tests
        find_maven_basedir = maven_wrapper.find_maven_basedir
    except ImportError as e2:
        logger.error(f"Second import attempt failed: {e2}")
        raise

def main():
    print("Maven Wrapper Test Script")
    print("-" * 40)
    
    # Find Maven base directory
    basedir = find_maven_basedir()
    print(f"Maven Base Directory: {basedir}")
    
    # Print available commands
    print("\nAvailable Commands:")
    print("1. Compile project (mvnw clean compile)")
    print("2. Run all tests (mvnw test)")
    print("3. Run specific test (mvnw test -Dtest=SomeTestName)")
    print("4. Run custom Maven command")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-4): ")
    
    if choice == "1":
        print("\nRunning Maven compile...")
        compile()
    elif choice == "2":
        print("\nRunning all Maven tests...")
        run_tests()
    elif choice == "3":
        test_name = input("Enter test name: ")
        print(f"\nRunning Maven test for {test_name}...")
        run_tests(test_name)
    elif choice == "4":
        command = input("Enter Maven command (e.g. 'clean package'): ")
        args = command.split()
        print(f"\nRunning Maven command: {command}...")
        run_maven(args)
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
