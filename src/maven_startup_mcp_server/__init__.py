"""Maven Startup MCP Server module.

Provides a Model Context Protocol (MCP) server that enables interaction with 
Maven build system functions (compile, test, package, etc.).
"""

from . import server
from .maven_wrapper import compile, run_tests, find_maven_basedir
import asyncio

def main():
   """Main entry point for the package."""
   asyncio.run(server.main())

# Expose important items at package level
__all__ = ['main', 'server', 'compile', 'run_tests', 'find_maven_basedir']