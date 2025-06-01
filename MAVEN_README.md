# Maven Startup MCP Server

This project provides Maven wrapper functionality integrated within an MCP server framework. It allows you to use Maven commands via Python and interact with Maven build processes through a Model Context Protocol (MCP) server.

## Features

- **Maven Wrapper Implementation**: Python-based equivalent of the Maven wrapper (`mvnw.cmd`)
- **MCP Server Integration**: Allows AI models to control Maven operations via a standardized protocol
- **Cross-Platform Support**: Works on Windows, Linux, and macOS
- **Project Management**: Streamlined Maven project management through a simple API

## Getting Started

### Setting Environment Variables

Before using the Maven wrapper functionality, set the `MAVEN_BASEDIR` environment variable to your Maven project's root directory:

#### Windows
```powershell
# Use the provided script
.\set_maven_env.ps1

# Or set manually
$env:MAVEN_BASEDIR = "path\to\your\maven\project"
```

#### Unix (Linux/macOS)
```bash
# Use the provided script
source ./set_maven_env.sh

# Or set manually
export MAVEN_BASEDIR=/path/to/your/maven/project
```

### Prerequisites

- Python 3.11 or higher
- Java Development Kit (JDK) installed and `JAVA_HOME` environment variable set
- Maven (optional - the wrapper can download Maven if not installed)

### Maven Wrapper Usage

#### Using Command-Line Scripts

```bash
# Run Maven compile
./mvnw clean compile

# Run all tests
./mvnw test

# Run a specific test
./mvnw test -Dtest=SomeTestName
```

#### Using Python Directly

```python
from maven_startup_mcp_server import compile, run_tests

# Compile the project
compile()

# Run all tests
run_tests()

# Run a specific test
run_tests("SomeTestName")
```

## MCP Server Integration

The Maven functionality is integrated into the MCP server, allowing AI assistants to perform Maven operations via standardized API calls.

### Available Tools

- `maven_compile`: Runs Maven clean compile
- `maven_test`: Runs Maven tests (all tests or a specific test)
- `maven_package`: Runs Maven package (with optional test skipping)
- `maven_run`: Runs any custom Maven command

### Available Resources

- `maven://project`: General project information
- `maven://pom`: The project's POM (Project Object Model) XML content
- `maven://modules`: List of project modules

## Configuration

### Maven Settings

Maven settings are read from:

1. Environment variables (`MAVEN_BASEDIR`, `JAVA_HOME`, etc.)
2. The `.mvn` directory in your project root
3. System defaults

## Contributing

We welcome contributions to improve the Maven wrapper functionality or the MCP server integration!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
