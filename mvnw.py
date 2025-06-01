#!/usr/bin/env python
"""
Maven wrapper command line interface.
Provides a Python-based equivalent for mvnw.cmd
"""

import sys
import os
import argparse
from pathlib import Path

# Add the src directory to the Python path
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from maven_startup_mcp_server.maven_wrapper import run_maven, compile, run_tests, find_maven_basedir

def main():
    """Main entry point for the Maven wrapper CLI."""
    parser = argparse.ArgumentParser(description="Maven Wrapper Python Implementation")
    parser.add_argument('--base-dir', dest='basedir', type=str, 
                        help='Override MAVEN_BASEDIR environment variable')
    parser.add_argument('--compile', action='store_true', 
                        help='Run Maven compile (equivalent to mvnw clean compile)')
    parser.add_argument('--test', action='store_true', 
                        help='Run Maven tests (equivalent to mvnw test)')
    parser.add_argument('--test-name', dest='test_name', type=str, 
                        help='Run a specific test (equivalent to mvnw test -Dtest=TestName)')
    parser.add_argument('maven_args', nargs='*', 
                        help='Raw Maven arguments to pass directly to Maven')
    
    args = parser.parse_args()
    
    # Set base directory if provided
    if args.basedir:
        os.environ["MAVEN_BASEDIR"] = args.basedir
    
    # Print current Maven base directory
    basedir = find_maven_basedir()
    print(f"Using Maven base directory: {basedir}")
    
    # Handle command options
    if args.compile:
        print("Running Maven compile...")
        return 0 if compile() else 1
    
    elif args.test or args.test_name:
        if args.test_name:
            print(f"Running Maven test for {args.test_name}...")
            return 0 if run_tests(args.test_name) else 1
        else:
            print("Running all Maven tests...")
            return 0 if run_tests() else 1
    
    # Raw Maven command execution
    elif args.maven_args:
        print(f"Executing Maven command: {' '.join(args.maven_args)}")
        return 0 if run_maven(args.maven_args) else 1
    
    else:
        parser.print_help()
        print("\nExamples:")
        print("  mvnw.py clean compile")
        print("  mvnw.py --compile")
        print("  mvnw.py test")
        print("  mvnw.py --test")
        print("  mvnw.py test -Dtest=SomeTestName")
        print("  mvnw.py --test-name SomeTestName")
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
