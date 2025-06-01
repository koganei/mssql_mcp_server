package com.example.app;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Test class for App.
 */
public class AppTest {
    
    @Test
    public void testAppGreeting() {
        App app = new App();
        assertNotNull(app.getGreeting(), "Greeting should not be null");
        assertEquals("Hello, Maven!", app.getGreeting(), "Greeting should match expected value");
    }
}
