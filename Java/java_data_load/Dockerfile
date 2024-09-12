# 使用一个基础的 Java 镜像
FROM openjdk:11-jre-slim

# 将 JAR 文件复制到容器中
COPY target/main-1.0-SNAPSHOT.jar /app.jar

# 指定启动应用程序的命令
ENTRYPOINT ["java", "-jar", "/app.jar"]


