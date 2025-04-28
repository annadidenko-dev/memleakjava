package org.example;

import java.util.ArrayList;
import java.util.List;

public class StaticMemoryLeakExample {

    private static final List<Object> cache = new ArrayList<>();

    public static void main(String[] args) {
        int counter = 0;

        for (int i = 0; i < 256; i++) {
            byte[] data = new byte[1024 * 1024]; // 1 MB
            cache.add(data);
            counter++;

            if (counter % 1000 == 0) {
                System.out.println("Cached objects: " + cache.size());
            }
        }
        for(;;);
    }
}
