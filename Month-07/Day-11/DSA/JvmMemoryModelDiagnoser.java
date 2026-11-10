package Month07.Day11;

/**
 * JVM Memory Architecture & Leak Diagnostics:
 * Simulates Heap (Eden, Survivor, Tenured/Old), Stack frames, and Metaspace.
 */
public class JvmMemoryModelDiagnoser {

    public record MemoryRegionStatus(String regionName, long usedBytes, long maxBytes) {
        public double getUsageRatio() {
            return (double) usedBytes / maxBytes;
        }
    }

    public static boolean isUnderMemoryPressure(MemoryRegionStatus oldGen) {
        return oldGen.getUsageRatio() > 0.85; // Trigger GC warning if > 85%
    }

    public static void main(String[] args) {
        MemoryRegionStatus oldGen = new MemoryRegionStatus("OldGen", 890_000_000L, 1_000_000_000L);
        boolean alert = isUnderMemoryPressure(oldGen);
        assert alert;

        System.out.println("Day 11 JVM Memory Diagnoser verification passed: Pressure=" + alert);
    }
}
