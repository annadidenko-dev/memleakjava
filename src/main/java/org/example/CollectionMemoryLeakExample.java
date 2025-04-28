package org.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class CollectionMemoryLeakExample {


    public static void main(String[] args) throws IOException {
        int counter = 0;
        Utils.waitForMemLeak();
        Map<String, String> cache = new HashMap<>();
        for (int i = 0; i < 1_000_000; i++) {
            String key = "key_" + counter;
            String value = "value_" + counter;

            // Добавляем элемент в коллекцию
            cache.put(key, value);

            counter++;

            // Периодически выводим размер коллекции
            if (counter % 10000 == 0) {
                System.out.println("Cache size: " + cache.size());
            }
        }

        for(;;);
    }
}
