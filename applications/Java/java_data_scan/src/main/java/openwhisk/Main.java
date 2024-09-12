package openwhisk;

import com.google.gson.*;
import redis.clients.jedis.*;
import redis.clients.jedis.params.ScanParams;
import redis.clients.jedis.resps.ScanResult;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;
import java.io.*;
import java.util.*;

public class Main {

    public static Map<String, String> readRedis(String name) {
        GenericObjectPoolConfig poolConfig = new GenericObjectPoolConfig();
        poolConfig.setMaxTotal(300);
        poolConfig.setMaxIdle(100);
        poolConfig.setMinIdle(1);
        Map<String, String> result = new HashMap<>();
        try (JedisPool pool = new JedisPool(poolConfig, "124.156.154.57", 6379, 30000, "openwhisk", 0);
             Jedis jedis = pool.getResource()) {
            ScanParams scanParams = new ScanParams().count(100);
            String cur = ScanParams.SCAN_POINTER_START;
            boolean cycleIsFinished = false;
            while (!cycleIsFinished) {
                ScanResult<Map.Entry<String, String>> scanResult = jedis.hscan(name, cur, scanParams);
                for (Map.Entry<String, String> entry : scanResult.getResult()) {
                    result.put(entry.getKey(), entry.getValue());
                }
                cur = scanResult.getCursor();
                if ("0".equals(cur)) {
                    cycleIsFinished = true;
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Can't read Redis: " + e);
        }
        return result;
    }

    public static JsonObject main(JsonObject args) {
        String filename = "10000_Sales_Records.csv";

        try {
            readRedis(filename);
        } catch (Exception e) {
            e.printStackTrace();
        }

        JsonObject output = new JsonObject();
        output.addProperty("result", filename + " read from Redis!");
        return output;
    }

    // Add the standard main method
    public static void main(String[] args) {
        JsonObject argsJson = new JsonObject();
        JsonObject result = main(argsJson);
        System.out.println(result.toString());
    }
}

