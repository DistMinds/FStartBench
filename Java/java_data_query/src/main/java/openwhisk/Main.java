package openwhisk;

import com.google.gson.*;
import redis.clients.jedis.*;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;
import java.io.*;
import java.util.*;

public class Main {

    public static List<String[]> readCsv(InputStream input) throws IOException {
        List<String[]> records = new ArrayList<>();
        try (InputStreamReader isReader = new InputStreamReader(input);
             BufferedReader reader = new BufferedReader(isReader)) {
            String str;
            while ((str = reader.readLine()) != null) {
                records.add(str.split(","));
            }
        }
        return records;
    }

    public static void writeRedis(List<String[]> records, String name) {
        GenericObjectPoolConfig poolConfig = new GenericObjectPoolConfig();
        poolConfig.setMaxTotal(300);
        poolConfig.setMaxIdle(100);
        poolConfig.setMinIdle(1);
        try (JedisPool pool = new JedisPool(poolConfig, "124.156.154.57", 6379, 30000, "openwhisk", 0);
             Jedis jedis = pool.getResource()) {
            Pipeline p = jedis.pipelined();
            for (int i = 1; i < records.size() - 1; i++) {
                p.hset(name, records.get(i)[6], records.get(i)[13]);
            }
            p.sync();
        } catch (Exception e) {
            throw new RuntimeException("Can't write Redis: " + e);
        }
    }

    public static JsonObject main(JsonObject args) {
        String filename = "10000_Sales_Records.csv";
        String local_path = "/";

        try (InputStream data = Main.class.getResourceAsStream(local_path + filename)) {
            if (data != null) {
                List<String[]> records = readCsv(data);
                writeRedis(records, filename);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        JsonObject output = new JsonObject();
        output.addProperty("result", filename + " write to Redis!");
        return output;
    }

    // Add the standard main method
    public static void main(String[] args) {
        JsonObject argsJson = new JsonObject();
        JsonObject result = main(argsJson);
        System.out.println(result.toString());
    }
}

