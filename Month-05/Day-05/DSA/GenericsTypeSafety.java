import java.util.*;

/**
 * Day 05: Java Generics & Type Safety
 * Implements generic pair/container classes, bounded type parameters (<T extends Comparable<T>>),
 * and wildcards (? extends Number vs ? super Integer).
 */
public class GenericsTypeSafety {

    static class Box<T extends Comparable<T>> {
        private T value;
        public Box(T value) { this.value = value; }
        public T getValue() { return value; }
        public boolean isGreaterThan(T other) {
            return this.value.compareTo(other) > 0;
        }
    }

    // Producer extends, Consumer super (PECS)
    public static double sumOfList(List<? extends Number> list) {
        double s = 0.0;
        for (Number n : list) s += n.doubleValue();
        return s;
    }

    public static void main(String[] args) {
        Box<Integer> intBox = new Box<>(42);
        assert intBox.isGreaterThan(10);

        Box<String> strBox = new Box<>("zebra");
        assert strBox.isGreaterThan("apple");

        List<Integer> ints = Arrays.asList(1, 2, 3);
        List<Double> doubles = Arrays.asList(1.5, 2.5);

        assert sumOfList(ints) == 6.0;
        assert sumOfList(doubles) == 4.0;

        System.out.println("Day 05 DSA GenericsTypeSafety verification passed!");
    }
}
