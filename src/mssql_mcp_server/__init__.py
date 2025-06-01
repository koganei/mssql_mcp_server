from . import server
import asyncio

# Import Maven functionality
try:
    from maven_startup_mcp_server.maven_wrapper import compile, run_tests, find_maven_basedir
    has_maven = True
except ImportError:
    has_maven = False

def main():
   """Main entry point for the package."""
   asyncio.run(server.main())

# Expose important items at package level
if has_maven:
    __all__ = ['main', 'server', 'compile', 'run_tests', 'find_maven_basedir']
else:
    __all__ = ['main', 'server']