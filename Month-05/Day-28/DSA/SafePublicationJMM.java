/**
 * Day 28: Concurrency — Java Memory Model & Safe Publication
 * Demonstrates the Double-Checked Locking pattern with volatile
 * ensuring happens-before visibility and preventing instruction reordering.
 */
public class SafePublicationJMM {

    private static volatile SafePublicationJMM instance;

    private SafePublicationJMM() {}

    public static SafePublicationJMM getInstance() {
        if (instance == null) {
            synchronized (SafePublicationJMM.class) {
                if (instance == null) {
                    instance = new SafePublicationJMM(); // volatile prevents partial initialization reordering!
                }
            }
        }
        return instance;
    }

    public static void main(String[] args) {
        SafePublicationJMM s1 = SafePublicationJMM.getInstance();
        SafePublicationJMM s2 = SafePublicationJMM.getInstance();
        assert s1 == s2 : "Must refer to identical singleton instance";
        System.out.println("Day 28 DSA SafePublicationJMM verification passed!");
    }
}
