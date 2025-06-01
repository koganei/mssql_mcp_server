import os
import sys
import logging
import subprocess
import platform
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("maven_startup_mcp_server.maven_wrapper")

# Environment variables
MAVEN_BASEDIR = os.getenv("MAVEN_BASEDIR", os.getcwd())
MAVEN_HOME = os.getenv("M2_HOME")
MAVEN_OPTS = os.getenv("MAVEN_OPTS", "")
MAVEN_DEBUG_OPTS = os.getenv("MAVEN_DEBUG_OPTS", "")
JAVA_HOME = os.getenv("JAVA_HOME")
MAVEN_BATCH_ECHO = os.getenv("MAVEN_BATCH_ECHO", "off")
MAVEN_BATCH_PAUSE = os.getenv("MAVEN_BATCH_PAUSE", "off")
MAVEN_SKIP_RC = os.getenv("MAVEN_SKIP_RC", "")

def print_if_echo_on(message):
    """Print message if MAVEN_BATCH_ECHO is on."""
    if MAVEN_BATCH_ECHO.lower() == "on":
        print(message)

def find_java():
    """Find Java in the system PATH if JAVA_HOME is not set."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run("where java", shell=True, check=False, 
                               text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split('\n')[0]
        else:
            result = subprocess.run("which java", shell=True, check=False, 
                               text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
    except Exception as e:
        logger.warning(f"Error checking for Java in PATH: {e}")
    
    return None

def validate_java_home():
    """Validate JAVA_HOME environment variable, or find Java in PATH."""
    # First check JAVA_HOME
    if JAVA_HOME:
        java_exe = Path(JAVA_HOME) / "bin" / ("java.exe" if platform.system() == "Windows" else "java")
        if java_exe.exists():
            logger.info(f"Using Java from JAVA_HOME: {java_exe}")
            return str(java_exe)
        else:
            logger.warning(f"JAVA_HOME is set to an invalid directory: {JAVA_HOME}")
    
    # Try to find Java in PATH
    java_path = find_java()
    if java_path:
        logger.info(f"Found Java in PATH: {java_path}")
        return java_path
    
    # If we get here, we couldn't find Java
    logger.error("Error: Java not found in your environment.")
    logger.error("Please install Java or set the JAVA_HOME variable in your environment.")
    raise ValueError("Java not found. Install Java or set JAVA_HOME environment variable.")

def find_maven_basedir():
    """Find the project base directory (containing .mvn folder)."""
    global MAVEN_BASEDIR
    
    if MAVEN_BASEDIR:
        logger.info(f"Using MAVEN_BASEDIR: {MAVEN_BASEDIR}")
        return MAVEN_BASEDIR
    
    # If not set, try to find .mvn directory by going up the directory tree
    current_dir = Path.cwd()
    while current_dir != current_dir.parent:  # Stop at root
        if (current_dir / ".mvn").exists():
            MAVEN_BASEDIR = str(current_dir)
            logger.info(f"Found MAVEN_BASEDIR: {MAVEN_BASEDIR}")
            return MAVEN_BASEDIR
        current_dir = current_dir.parent
    
    # If not found, use current directory
    MAVEN_BASEDIR = str(Path.cwd())
    logger.info(f"Using current directory as MAVEN_BASEDIR: {MAVEN_BASEDIR}")
    return MAVEN_BASEDIR

def get_wrapper_jar():
    """Get the path to the Maven wrapper JAR file."""
    base_dir = find_maven_basedir()
    wrapper_jar = Path(base_dir) / ".mvn" / "wrapper" / "maven-wrapper.jar"
    return str(wrapper_jar)

def check_maven_installation():
    """Check if Maven is installed and accessible."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run("where mvn", shell=True, check=False, 
                                   text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run("which mvn", shell=True, check=False, 
                                   text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return result.returncode == 0
    except Exception:
        return False

def download_maven_wrapper(base_dir):
    """Download Maven wrapper JAR and properties if they don't exist."""
    logger.info("Maven wrapper JAR not found. Attempting to download it...")
    
    wrapper_dir = Path(base_dir) / ".mvn" / "wrapper"
    wrapper_jar = wrapper_dir / "maven-wrapper.jar"
    wrapper_props = wrapper_dir / "maven-wrapper.properties"
    
    if not wrapper_dir.exists():
        wrapper_dir.mkdir(parents=True, exist_ok=True)
    
    if not wrapper_props.exists():
        wrapper_props_content = """distributionUrl=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.6/apache-maven-3.9.6-bin.zip
wrapperUrl=https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar
"""
        with open(wrapper_props, 'w') as f:
            f.write(wrapper_props_content)
        logger.info(f"Created Maven wrapper properties at {wrapper_props}")
    
    # Download wrapper JAR using Python
    if not wrapper_jar.exists():
        try:
            import urllib.request
            wrapper_url = "https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar"
            logger.info(f"Downloading Maven wrapper from {wrapper_url}")
            urllib.request.urlretrieve(wrapper_url, wrapper_jar)
            logger.info(f"Maven wrapper JAR downloaded to {wrapper_jar}")
            return True
        except Exception as e:
            logger.error(f"Failed to download Maven wrapper: {e}")
            return False
    return True

def get_maven_command():
    """Get the Maven command to use."""
    # Get project base directory
    maven_basedir = find_maven_basedir()
    
    # Try M2_HOME first if set
    if MAVEN_HOME:
        if platform.system() == "Windows":
            maven_cmd = str(Path(MAVEN_HOME) / "bin" / "mvn.cmd")
        else:
            maven_cmd = str(Path(MAVEN_HOME) / "bin" / "mvn")
        
        if Path(maven_cmd).exists():
            logger.info(f"Using Maven from M2_HOME: {maven_cmd}")
            return maven_cmd
    
    # Try to use wrapper if it exists
    wrapper_jar = get_wrapper_jar()
    wrapper_jar_path = Path(wrapper_jar)
    
    if wrapper_jar_path.exists():
        try:
            java_exe = validate_java_home()
            logger.info(f"Using Maven wrapper with Java: {java_exe}")
            return f"{java_exe} {MAVEN_OPTS} {MAVEN_DEBUG_OPTS} -Dmaven.multiModuleProjectDirectory=\"{maven_basedir}\" -classpath \"{wrapper_jar}\" org.apache.maven.wrapper.MavenWrapperMain"
        except Exception as e:
            logger.error(f"Failed to use Maven wrapper: {e}")
    else:
        # Try to download Maven wrapper
        if download_maven_wrapper(maven_basedir):
            try:
                java_exe = validate_java_home()
                logger.info(f"Using downloaded Maven wrapper with Java: {java_exe}")
                return f"{java_exe} {MAVEN_OPTS} {MAVEN_DEBUG_OPTS} -Dmaven.multiModuleProjectDirectory=\"{maven_basedir}\" -classpath \"{wrapper_jar}\" org.apache.maven.wrapper.MavenWrapperMain"
            except Exception as e:
                logger.error(f"Failed to use downloaded Maven wrapper: {e}")
    
    # Try system mvn as last resort
    if check_maven_installation():
        if platform.system() == "Windows":
            logger.info("Using system Maven (mvn.cmd)")
            return f"mvn.cmd \"-Dmaven.multiModuleProjectDirectory={maven_basedir}\""
        else:
            logger.info("Using system Maven (mvn)")
            return f"mvn \"-Dmaven.multiModuleProjectDirectory={maven_basedir}\""
    
    logger.warning("Maven not found! Using mvn command but it will likely fail.")
    logger.warning("Please install Maven or provide JAVA_HOME to use the wrapper.")
    
    # Return a command that will just display a more helpful error
    if platform.system() == "Windows":
        return f"mvn.cmd \"-Dmaven.multiModuleProjectDirectory={maven_basedir}\""
    return f"mvn \"-Dmaven.multiModuleProjectDirectory={maven_basedir}\""

def run_maven(args):
    """Run Maven with the specified arguments."""
    if not isinstance(args, list):
        args = args.split()
    
    # Check Java installation first
    try:
        java_installed = False
        if JAVA_HOME:
            java_exe = Path(JAVA_HOME) / "bin" / ("java.exe" if platform.system() == "Windows" else "java")
            if java_exe.exists():
                java_installed = True
        
        if not java_installed:
            # Try to check if java is in PATH
            try:
                if platform.system() == "Windows":
                    result = subprocess.run("where java", shell=True, check=False, 
                                          text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    result = subprocess.run("which java", shell=True, check=False, 
                                          text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                java_installed = result.returncode == 0
            except Exception:
                pass
        
        if not java_installed:
            logger.error("Java not found. Please install Java or set JAVA_HOME.")
            print("ERROR: Java not found. Please install Java or set JAVA_HOME.")
            return False
    
    except Exception as e:
        logger.error(f"Error checking Java installation: {e}")
    
    cmd = get_maven_command()
    full_command = f"{cmd} {' '.join(args)}"
    
    logger.info(f"Executing: {full_command}")
    
    # Change to the Maven base directory
    original_dir = os.getcwd()
    maven_basedir = find_maven_basedir()
    os.chdir(maven_basedir)
    
    try:
        logger.info(f"Running Maven in directory: {maven_basedir}")
        result = subprocess.run(full_command, shell=True, check=True, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            logger.warning(result.stderr)
        
        if MAVEN_BATCH_PAUSE.lower() == "on":
            input("Press Enter to continue...")
        
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Maven execution failed: {e}")
        
        # Print command output even if it failed
        if hasattr(e, 'stdout') and e.stdout:
            print(e.stdout)
        
        if hasattr(e, 'stderr') and e.stderr:
            logger.error(e.stderr)
        
        # Provide specific guidance based on error
        if "not recognized as an internal or external command" in str(e):
            logger.error("Maven is not installed or not in PATH. Please install Maven or use the Maven wrapper.")
            print("\nERROR: Maven is not installed or not in PATH.")
            print("To fix this, you can either:")
            print("1. Install Maven and add it to your PATH")
            print("2. Set the M2_HOME environment variable to your Maven installation")
            print("3. Make sure JAVA_HOME is set correctly to use the Maven wrapper\n")
        
        if MAVEN_BATCH_PAUSE.lower() == "on":
            input("Press Enter to continue...")
        
        return False
    except Exception as e:
        logger.error(f"Unexpected error running Maven: {e}")
        return False
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

def compile():
    """Run mvnw clean compile."""
    logger.info("Running Maven compile...")
    return run_maven(["clean", "compile"])

def run_tests(test_name=None):
    """
    Run Maven tests.
    If test_name is provided, runs only that specific test.
    """
    if test_name:
        logger.info(f"Running specific test: {test_name}...")
        return run_maven(["test", f"-Dtest={test_name}"])
    else:
        logger.info("Running all tests...")
        return run_maven(["test"])

if __name__ == "__main__":
    # Handle direct invocation like the mvnw.cmd script
    if len(sys.argv) > 1:
        run_maven(sys.argv[1:])
    else:
        print("Maven Wrapper Python Implementation")
        print("Usage: python maven_wrapper.py [maven_commands]")
        print("Examples:")
        print("  python maven_wrapper.py clean compile")
        print("  python maven_wrapper.py test")
        print("  python maven_wrapper.py test -Dtest=SomeTestName")
