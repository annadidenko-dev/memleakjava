package org.example;

public class Utils {
    public static void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public static void waitForMemLeak() {
        System.out.println("Memory leak will be produced in 30 seconds");
        sleep(30 * 1000);
        System.out.println("Producing memory leak");
    }

    public static void memoryLeaked() {
        System.out.println("Memory leak produced");
        while (true) {

        }
    }
}
