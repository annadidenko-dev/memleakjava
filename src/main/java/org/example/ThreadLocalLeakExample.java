package org.example;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ThreadLocalLeakExample {

    private static final ExecutorService executor = Executors.newFixedThreadPool(100);
    private static final ThreadLocal<byte[]> threadLocal = new ThreadLocal<>();

    public static void main(String[] args) {
        while (true) {
            executor.submit(() -> {
                // Создаем большой объект и кладем его в ThreadLocal
                byte[] largeData = new byte[10 * 1024 * 1024]; // 10 MB
                threadLocal.set(largeData);

                // Не вызываем threadLocal.remove() — это ключевая ошибка
                System.out.println("Thread " + Thread.currentThread().getName() + " stored large object");
            });

            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
