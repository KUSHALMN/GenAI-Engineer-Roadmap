package Month07.Day25;

import java.util.Collections;
import java.util.List;

/**
 * Enterprise Java Patterns:
 * Defensive copying, unmodifiable collections, and immutability invariants.
 */
public class EnterpriseJavaCodingPatterns {

    public static final class ImmutableTenantPolicy {
        private final String tenantId;
        private final List<String> allowedScopes;

        public ImmutableTenantPolicy(String tenantId, List<String> scopes) {
            this.tenantId = tenantId;
            // Defensive copy
            this.allowedScopes = Collections.unmodifiableList(List.copyOf(scopes));
        }

        public String getTenantId() { return tenantId; }
        public List<String> getAllowedScopes() { return allowedScopes; }
    }

    public static void main(String[] args) {
        List<String> mutableList = new java.util.ArrayList<>();
        mutableList.add("read");
        ImmutableTenantPolicy policy = new ImmutableTenantPolicy("corp-1", mutableList);

        mutableList.add("write"); // Modifying original list does NOT mutate policy!
        assert policy.getAllowedScopes().size() == 1;

        System.out.println("Day 25 Enterprise Java Coding Patterns verification passed.");
    }
}
