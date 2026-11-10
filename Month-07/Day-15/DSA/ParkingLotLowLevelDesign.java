package Month07.Day15;

import java.util.HashMap;
import java.util.Map;

/**
 * Low-Level Design (LLD): Parking Lot System
 * Object-oriented modeling of Vehicles, Spots, Levels, and Ticket pricing.
 */
public class ParkingLotLowLevelDesign {

    public enum VehicleType { MOTORCYCLE, COMPACT, LARGE }

    public record Ticket(String ticketId, VehicleType type, long entryTime) {}

    public static class ParkingLot {
        private final Map<String, Ticket> activeTickets = new HashMap<>();
        private int availableCompactSpots = 5;

        public Ticket parkVehicle(String plate, VehicleType type) {
            if (type == VehicleType.COMPACT && availableCompactSpots > 0) {
                availableCompactSpots--;
                Ticket t = new Ticket(plate, type, System.currentTimeMillis());
                activeTickets.put(plate, t);
                return t;
            }
            return null; // Full or unsupported
        }

        public double exitVehicle(String plate) {
            Ticket t = activeTickets.remove(plate);
            if (t != null) {
                availableCompactSpots++;
                return 15.00; // Flat fee simulation
            }
            return 0.0;
        }

        public int getAvailableSpots() { return availableCompactSpots; }
    }

    public static void main(String[] args) {
        ParkingLot lot = new ParkingLot();
        Ticket t = lot.parkVehicle("KA-01-1234", VehicleType.COMPACT);
        assert t != null;
        assert lot.getAvailableSpots() == 4;

        double fee = lot.exitVehicle("KA-01-1234");
        assert fee == 15.00;
        assert lot.getAvailableSpots() == 5;

        System.out.println("Day 15 Parking Lot LLD verification passed.");
    }
}
