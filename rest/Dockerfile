# [1] https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.11-slim-bookworm

# [2] Виставляємо робочу директорію контейнера в /app
WORKDIR /app

# [3] Виставляємо OpenJDK JRE - потрібно для Flyway, встановлення конкретно 11ої версії не спрацювало
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Зазначаємо Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# [4] Встановлюємо Flyway
ENV FLYWAY_VERSION=10.7.1
RUN apt-get update && \
    apt-get install -y wget && \
    wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/${FLYWAY_VERSION}/flyway-commandline-${FLYWAY_VERSION}.tar.gz | tar xvz && \
    ln -s $(pwd)/flyway-${FLYWAY_VERSION}/flyway /usr/local/bin/flyway && \
    apt-get remove -y wget && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

ENV FLYWAY_BASELINE_ON_MIGRATE=true

# [5] Копіюємо файл з залежностями, створюється новий шар
COPY requirements.txt requirements.txt

# [6] Встановлюємо залежності вказалі requirements.txt - теж новий шор
RUN pip install --no-cache-dir -r requirements.txt

# [7] Копіюємо файли міграції
COPY ./db/migration /flyway/sql/
ENV FLYWAY_LOCATIONS=filesystem:/flyway/sql/

# [8] Додаємо наш код /app - створили новий шар. таким чином при ребілді не потрібно заново ставити залежності при змані коду
COPY . /app

# Документуємо порт, що використовується контейнером. В компоузі буде юзатися для міжконтейнерного зв'язку
EXPOSE 5000

# Perform flyway migration and run run.py when the container launches
# https://spacelift.io/blog/docker-entrypoint-vs-cmd
CMD ["sh", "-c", "flyway migrate && python run.py"]
