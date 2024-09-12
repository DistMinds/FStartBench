FROM openjdk:8-jdk-alpine
# 更新包列表并安装 OpenJDK 11
#RUN apt-get update && \
#    apt-get install -y openjdk-17-jdk && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*


# 将 JAR 文件复制到容器中
COPY target/main-1.0-SNAPSHOT.jar /app.jar

# 指定启动应用程序的命令
ENTRYPOINT ["java", "-jar", "/app.jar"]

