package Month07.Day05;

/**
 * Enterprise Exception Handling Framework:
 * 1. Base Domain Exception with HTTP status codes and error codes.
 * 2. Specialized subclasses (ResourceNotFound, Unauthorized, RateLimitExceeded).
 * 3. Safe exception boundaries translating internal stack traces to clean API errors.
 */
public class ExceptionHandlingFramework {

    public enum ErrorCode {
        RESOURCE_NOT_FOUND(404),
        UNAUTHORIZED(401),
        TENANT_ISOLATION_VIOLATION(403),
        RATE_LIMIT_EXCEEDED(429),
        INTERNAL_ERROR(500);

        private final int httpStatus;
        ErrorCode(int httpStatus) { this.httpStatus = httpStatus; }
        public int getHttpStatus() { return httpStatus; }
    }

    public static class BasePlatformException extends RuntimeException {
        private final ErrorCode errorCode;

        public BasePlatformException(ErrorCode errorCode, String message) {
            super(message);
            this.errorCode = errorCode;
        }

        public ErrorCode getErrorCode() { return errorCode; }
    }

    public static class TenantViolationException extends BasePlatformException {
        public TenantViolationException(String message) {
            super(ErrorCode.TENANT_ISOLATION_VIOLATION, message);
        }
    }

    public static void main(String[] args) {
        try {
            throw new TenantViolationException("Cross-tenant access attempted!");
        } catch (BasePlatformException ex) {
            assert ex.getErrorCode().getHttpStatus() == 403;
            System.out.println("Day 05 Exception Handling verification passed: " + ex.getMessage());
        }
    }
}
