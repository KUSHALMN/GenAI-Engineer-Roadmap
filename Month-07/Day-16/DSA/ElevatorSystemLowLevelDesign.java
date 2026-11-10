package Month07.Day16;

import java.util.TreeSet;

/**
 * Low-Level Design (LLD): Elevator System
 * Models Elevator state transitions, directional queues (LOOK / SCAN algorithm).
 */
public class ElevatorSystemLowLevelDesign {

    public enum Direction { UP, DOWN, IDLE }

    public static class Elevator {
        private int currentFloor = 1;
        private Direction direction = Direction.IDLE;
        private final TreeSet<Integer> upRequests = new TreeSet<>();
        private final TreeSet<Integer> downRequests = new TreeSet<>();

        public void addRequest(int floor) {
            if (floor > currentFloor) {
                upRequests.add(floor);
            } else if (floor < currentFloor) {
                downRequests.add(floor);
            }
        }

        public void step() {
            if (!upRequests.isEmpty()) {
                direction = Direction.UP;
                currentFloor = upRequests.pollFirst();
            } else if (!downRequests.isEmpty()) {
                direction = Direction.DOWN;
                currentFloor = downRequests.pollLast();
            } else {
                direction = Direction.IDLE;
            }
        }

        public int getCurrentFloor() { return currentFloor; }
        public Direction getDirection() { return direction; }
    }

    public static void main(String[] args) {
        Elevator elevator = new Elevator();
        elevator.addRequest(5);
        elevator.addRequest(3);

        elevator.step();
        assert elevator.getCurrentFloor() == 3;
        assert elevator.getDirection() == Direction.UP;

        elevator.step();
        assert elevator.getCurrentFloor() == 5;

        System.out.println("Day 16 Elevator System LLD verification passed.");
    }
}
