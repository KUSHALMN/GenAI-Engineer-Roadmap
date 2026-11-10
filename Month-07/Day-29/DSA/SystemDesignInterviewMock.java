package Month07.Day29;

import java.util.HashMap;
import java.util.Map;

/**
 * 60-Minute LLD Mock: Scalable URL Shortener
 * Base62 encoding, hash collisions, and URL redirection registry.
 */
public class SystemDesignInterviewMock {

    private static final String BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private final Map<String, String> shortToLong = new HashMap<>();
    private long autoIncrementId = 100000;

    public String encode(String longUrl) {
        long id = autoIncrementId++;
        StringBuilder sb = new StringBuilder();
        while (id > 0) {
            sb.append(BASE62.charAt((int)(id % 62)));
            id /= 62;
        }
        String shortCode = sb.reverse().toString();
        shortToLong.put(shortCode, longUrl);
        return "https://tiny.ai/" + shortCode;
    }

    public String decode(String shortUrl) {
        String code = shortUrl.replace("https://tiny.ai/", "");
        return shortToLong.get(code);
    }

    public static void main(String[] args) {
        SystemDesignInterviewMock shortener = new SystemDesignInterviewMock();
        String original = "https://genai.enterprise.platform/models/v3/deepseek-r1";
        String tiny = shortener.encode(original);

        assert tiny.startsWith("https://tiny.ai/");
        assert shortener.decode(tiny).equals(original);

        System.out.println("Day 29 System Design Interview Mock verification passed: " + tiny);
    }
}
