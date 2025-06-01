package com.example.app;

/**
 * Simple Java application to demonstrate Maven compilation.
 */
public class App {
    
    /**
     * Returns a greeting message.
     * @return A greeting string
     */
    public String getGreeting() {
        return "Hello, Maven!";
    }
    
    /**
     * Main entry point for the application.
     * @param args Command line arguments
     */
    public static void main(String[] args) {
        App app = new App();
        System.out.println(app.getGreeting());
    }
}
