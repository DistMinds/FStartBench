package openwhisk;

import com.google.gson.JsonObject;
import redis.clients.jedis.*;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

import java.io.*;
import java.util.*;

public class Main {

    public static List<String[]> readCsv(InputStream input) throws IOException {
        List<String[]> records = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(input))) {
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
            throw new RuntimeException("Can't write to Redis: " + e.getMessage(), e);
        }
    }

    // 将原来的 main 方法重命名为 processFile
    public static JsonObject processFile(JsonObject args) {
        String filename = "10000_Sales_Records.csv";
        String localPath = "/";

        try (InputStream data = Main.class.getResourceAsStream(localPath + filename)) {
            if (data == null) {
                throw new FileNotFoundException("File not found: " + localPath + filename);
            }
            List<String[]> records = readCsv(data);
            writeRedis(records, filename);
        } catch (Exception e) {
            e.printStackTrace();
            JsonObject errorOutput = new JsonObject();
            errorOutput.addProperty("error", "Failed to process the file: " + e.getMessage());
            return errorOutput;
        }

        JsonObject output = new JsonObject();
        output.addProperty("result", filename + " written to Redis!");
        return output;
    }

    // 添加标准的 main 方法
    public static void main(String[] args) {
        // 示例: 如果你想从命令行参数中获取文件名，可以在这里处理
        JsonObject argsJson = new JsonObject();
        // 你可以将 args 转换为 JsonObject 或者根据需要进行处理

        JsonObject result = processFile(argsJson);
        System.out.println(result.toString());
    }
}



