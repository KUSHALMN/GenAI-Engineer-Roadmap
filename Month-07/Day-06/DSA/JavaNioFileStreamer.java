package Month07.Day06;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

/**
 * Java I/O and NIO Stream Processing:
 * Zero-copy buffer streaming, channel reads, and byte chunk allocation.
 */
public class JavaNioFileStreamer {

    public static int streamAndCountBytes(InputStream input, int bufferCapacity) throws Exception {
        int totalBytes = 0;
        try (ReadableByteChannel channel = Channels.newChannel(input)) {
            ByteBuffer buffer = ByteBuffer.allocate(bufferCapacity);
            while (channel.read(buffer) > 0) {
                buffer.flip(); // Prepare buffer for reading
                totalBytes += buffer.remaining();
                buffer.clear(); // Reset for next channel read
            }
        }
        return totalBytes;
    }

    public static void main(String[] args) throws Exception {
        byte[] payload = "High-throughput LLMOps streaming buffer".getBytes();
        InputStream stream = new ByteArrayInputStream(payload);
        int counted = streamAndCountBytes(stream, 16);
        assert counted == payload.length;

        System.out.println("Day 06 Java NIO streaming verification passed: " + counted + " bytes.");
    }
}
