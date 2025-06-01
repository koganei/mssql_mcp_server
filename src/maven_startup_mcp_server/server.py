import asyncio
import logging
import os
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from pydantic import AnyUrl
from .maven_wrapper import compile, run_tests, find_maven_basedir

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("maven_startup_mcp_server")

# Initialize server
app = Server("maven_startup_mcp_server")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List Maven resources."""
    # Add Maven resource
    maven_basedir = find_maven_basedir()
    resources = [
        Resource(
            uri="maven://project",
            name="Maven Project",
            mimeType="text/plain",
            description=f"Maven project at {maven_basedir}"
        ),
        Resource(
            uri="maven://pom",
            name="Maven POM",
            mimeType="text/xml",
            description="Project Object Model (POM) file"
        ),
        Resource(
            uri="maven://modules",
            name="Maven Modules",
            mimeType="text/plain",
            description="Maven project modules"
        )
    ]
    return resources

@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read Maven resource contents."""
    uri_str = str(uri)
    logger.info(f"Reading resource: {uri_str}")
    
    if uri_str == "maven://project":
        maven_basedir = find_maven_basedir()
        return f"Maven project information:\nBase directory: {maven_basedir}\n"
    
    elif uri_str == "maven://pom":
        maven_basedir = find_maven_basedir()
        pom_path = os.path.join(maven_basedir, "pom.xml")
        
        try:
            with open(pom_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "POM file not found. Make sure this is a Maven project."
        except Exception as e:
            logger.error(f"Error reading POM file: {str(e)}")
            return f"Error reading POM file: {str(e)}"
    
    elif uri_str == "maven://modules":
        maven_basedir = find_maven_basedir()
        modules = []
        
        # Check for src/main and src/test directories
        src_main = os.path.join(maven_basedir, "src", "main")
        src_test = os.path.join(maven_basedir, "src", "test")
        
        if os.path.exists(src_main):
            modules.append("main")
        if os.path.exists(src_test):
            modules.append("test")
            
        return f"Maven project modules:\n" + "\n".join(modules)
    
    else:
        raise ValueError(f"Invalid URI scheme: {uri_str}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Maven tools."""
    logger.info("Listing tools...")
    return [
        Tool(
            name="maven_compile",
            description="Run Maven compile (equivalent to mvnw clean compile)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="maven_test",
            description="Run Maven tests (equivalent to mvnw test)",
            inputSchema={
                "type": "object",
                "properties": {
                    "test_name": {
                        "type": "string",
                        "description": "Optional specific test name to run (equivalent to -Dtest=TestName)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="maven_package",
            description="Run Maven package (equivalent to mvnw package)",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip_tests": {
                        "type": "boolean",
                        "description": "Optional flag to skip tests during packaging"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="maven_run",
            description="Run custom Maven command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Maven command to run (without 'mvnw' prefix)"
                    }
                },
                "required": ["command"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Maven operations."""
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    
    if name == "maven_compile":
        logger.info("Running Maven compile...")
        success = compile()
        if success:
            return [TextContent(type="text", text="Maven compile completed successfully.")]
        else:
            return [TextContent(type="text", text="Maven compile failed. Check logs for details.")]
    
    elif name == "maven_test":
        test_name = arguments.get("test_name")
        if test_name:
            logger.info(f"Running Maven test for {test_name}...")
            success = run_tests(test_name)
            if success:
                return [TextContent(type="text", text=f"Maven test for {test_name} completed successfully.")]
            else:
                return [TextContent(type="text", text=f"Maven test for {test_name} failed. Check logs for details.")]
        else:
            logger.info("Running all Maven tests...")
            success = run_tests()
            if success:
                return [TextContent(type="text", text="Maven tests completed successfully.")]
            else:
                return [TextContent(type="text", text="Maven tests failed. Check logs for details.")]
    
    elif name == "maven_package":
        skip_tests = arguments.get("skip_tests", False)
        logger.info(f"Running Maven package (skip_tests={skip_tests})...")
        
        cmd = ["package"]
        if skip_tests:
            cmd.append("-DskipTests")
            
        # Use the run_maven function from maven_wrapper
        from .maven_wrapper import run_maven
        success = run_maven(cmd)
        
        if success:
            return [TextContent(type="text", text="Maven package completed successfully.")]
        else:
            return [TextContent(type="text", text="Maven package failed. Check logs for details.")]
    
    elif name == "maven_run":
        command = arguments.get("command")
        if not command:
            raise ValueError("Command is required")
        
        logger.info(f"Running Maven command: {command}...")
        
        # Use the run_maven function from maven_wrapper
        from .maven_wrapper import run_maven
        success = run_maven(command.split())
        
        if success:
            return [TextContent(type="text", text=f"Maven command '{command}' completed successfully.")]
        else:
            return [TextContent(type="text", text=f"Maven command '{command}' failed. Check logs for details.")]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Maven MCP server...")
    
    # Log Maven configuration
    maven_basedir = find_maven_basedir()
    logger.info(f"Maven base directory: {maven_basedir}")
    
    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            logger.error(f"Server error: {str(e)}", exc_info=True)
            raise

if __name__ == "__main__":
    asyncio.run(main())
