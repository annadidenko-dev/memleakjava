package org.example;

import java.util.Timer;
import java.util.TimerTask;

public class TimerLeakExample {

    static class LeakyTask extends TimerTask {
        private final byte[] bigData = new byte[10 * 1024 * 1024]; // 10 MB

        @Override
        public void run() {
            System.out.println("Task running: " + this);
        }
    }

    public static void main(String[] args) {
        Timer timer = new Timer();

        while (true) {
            TimerTask task = new LeakyTask();
            timer.schedule(task, 1000); // Однократное выполнение с задержкой

            try {
                Thread.sleep(10); // Небольшая задержка между созданием задач
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
