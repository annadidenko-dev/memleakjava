package org.example;

import java.util.ArrayList;
import java.util.List;

import static org.example.Utils.memoryLeaked;
import static org.example.Utils.waitForMemLeak;

public class EventLeakExample {
    public static void main(String[] args) {
        waitForMemLeak();

        EventSource source = new EventSource();

        for (int i = 0; i < 1_000_000; i++) {
            // Каждый раз создаём новый listener и добавляем его
            EventListener listener = new MyListener();
            source.addListener(listener);

            if (i % 100_000 == 0) {
                System.out.println("Listeners count: " + source.getListenerCount());
                System.gc();
            }
        }
        memoryLeaked();

    }

    interface EventListener {
        void onEvent(String data);
    }

    static class MyListener implements EventListener {
        private final byte[] bigData = new byte[1024]; // 1 KiB

        @Override
        public void onEvent(String data) {
            // ничего не делаем
        }
    }

    static class EventSource {
        private final List<EventListener> listeners = new ArrayList<>();

        public void addListener(EventListener listener) {
            listeners.add(listener);
        }

        public int getListenerCount() {
            return listeners.size();
        }
    }
}
