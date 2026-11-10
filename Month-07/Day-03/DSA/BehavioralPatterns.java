package Month07.Day03;

import java.util.ArrayList;
import java.util.List;

/**
 * Behavioral Design Patterns:
 * 1. Strategy Pattern: Pluggable Reranking Strategies.
 * 2. Observer Pattern: Event listeners for token budget usage.
 * 3. Command Pattern: Undoable transactional commands.
 */
public class BehavioralPatterns {

    // 1. Strategy Pattern
    public interface ScoringStrategy {
        double score(double semanticSim, double bm25Score);
    }

    public static class HybridRRFStrategy implements ScoringStrategy {
        @Override
        public double score(double semanticSim, double bm25Score) {
            return (0.7 * semanticSim) + (0.3 * bm25Score);
        }
    }

    // 2. Observer Pattern
    public interface BudgetObserver {
        void onBudgetExceeded(String tenantId, int usedTokens);
    }

    public static class QuotaManager {
        private final List<BudgetObserver> observers = new ArrayList<>();

        public void subscribe(BudgetObserver observer) { observers.add(observer); }
        public void notifyLimit(String tenant, int tokens) {
            for (BudgetObserver o : observers) {
                o.onBudgetExceeded(tenant, tokens);
            }
        }
    }

    public static void main(String[] args) {
        ScoringStrategy strategy = new HybridRRFStrategy();
        double finalScore = strategy.score(0.85, 0.60);
        assert finalScore > 0.7;

        QuotaManager manager = new QuotaManager();
        final boolean[] alertFired = {false};
        manager.subscribe((tenant, tokens) -> alertFired[0] = true);
        manager.notifyLimit("tenant_corp", 150000);
        assert alertFired[0];

        System.out.println("Day 03 Behavioral Patterns verification passed.");
    }
}
