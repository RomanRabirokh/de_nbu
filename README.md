# Project Overview (EN)

## Description

This project is a data pipeline built with **Apache Airflow** and **Python** that fetches currency exchange rates from the **NBU (National Bank of Ukraine) public API**, validates and transforms the data, and stores it in **ClickHouse** for further analysis.

The pipeline is fully containerized with **Docker Compose** and is designed to be easy to initialize and run locally in a development environment.

Main responsibilities of the project:

* Fetch exchange rate data from the NBU API
* Validate incoming data (using Pydantic models)
* Transform and normalize the data
* Orchestrate the workflow using Airflow DAGs
* Persist processed data into ClickHouse

---

## Technology Stack

* **Python 3**
* **Apache Airflow** – workflow orchestration
* **ClickHouse** – analytical database
* **Docker & Docker Compose** – local environment and services
* **Poetry** – Python dependency management
* **Pydantic** – data validation and schema enforcement

---

## Airflow

The project includes an **Airflow Web UI (Admin Panel)** that allows you to:

* Monitor DAG execution
* Trigger DAGs manually
* Inspect task logs
* Manage connections and variables

Airflow is initialized automatically during the first project setup.

Open in browser:

```
http://localhost:8080
```

Login credentials:

* Username: `admin`
* Password: `admin`


### DAG execution behavior

The `nbu_rates` DAG is configured with:

* `schedule_interval = "@daily"`
* `start_date = 2026-01-01`
* `catchup = true`

Meaning:

* DAG runs are automatically created by the scheduler
* Missed runs since `start_date` will be executed
* Manual triggering is optional

---

## Step-by-step run

### 1. Prepare environment and start containers

```bash
make up
```

* If `.env` does not exist, this will:

  * Run `make init` to create `.env` and `docker-compose.yml`
  * Initialize Airflow (DB + admin user)
  * Apply ClickHouse migrations
  * Start all Docker containers in the background

---

### 2. Verify data in ClickHouse

```bash
make check-rates
```

* Check that processed data is stored

---

### 3. Stop or clean up

**Stop containers (keep data):**

```bash
make stop
```

**Completely remove containers and data:**

```bash
make destroy
```

---

## Description of commands

### First-time setup (run only once)

```bash
make init
```

This command performs the full initial setup:

1. Copies the development Docker Compose configuration:

   * `docker/dev/docker-compose.yml` → `./docker-compose.yml`
2. Copies the development environment variables:

   * `env/.env.dev` → `./.env`

---

### Airflow Initialization (internal command)

```bash
make airflow-init
```

Used internally by `make init`. It:

* Upgrades the Airflow metadata database
* Creates an admin user using credentials from `.env`

---

### Apply ClickHouse Migrations

```bash
make migrate-up
```

* Executes all SQL files from `src/migrations/clickhouse/`
* Applies schema changes to ClickHouse
* Uses ClickHouse credentials from environment variables

---

### Install / Run Python Commands (Poetry)

```bash
make poentry CMD="add requests"
```

* Executes Poetry commands inside the Airflow container
* Useful for installing or managing Python dependencies

---

### Check Loaded Rates in ClickHouse

```bash
make check-rates
```

* Runs a test SQL query against ClickHouse
* Displays stored exchange rates in the console

---

### Destroy Environment

```bash
make destroy
```

* Stops all containers
* Removes volumes, images, and orphan containers
* Completely resets the project state

---

## Environment Configuration

All environment variables are stored in the `.env` file, including:

* Airflow admin credentials
* ClickHouse connection parameters
* Service configuration

---

## Notes

* Currently, only the **dev** environment is supported
* All services run inside Docker containers
* The project is intended for local development and experimentation

---

---

# Опис проєкту (UA)

## Загальний опис

Цей проєкт — це **data pipeline**, побудований на **Apache Airflow** та **Python**, який отримує курси валют з **публічного API НБУ**, валідуює та трансформує дані, після чого зберігає їх у **ClickHouse** для подальшого аналізу.

Проєкт повністю контейнеризований за допомогою **Docker Compose** і розрахований на простий запуск у локальному середовищі розробки.

Основні задачі проєкту:

* Отримання курсів валют з API НБУ
* Валідація вхідних даних (за допомогою Pydantic)
* Трансформація та нормалізація даних
* Оркестрація процесів через Airflow DAG-и
* Збереження оброблених даних у ClickHouse

---

## Технології

* **Python 3**
* **Apache Airflow** — оркестрація workflow
* **ClickHouse** — аналітична база даних
* **Docker & Docker Compose** — середовище виконання
* **Poetry** — керування Python-залежностями
* **Pydantic** — валідація та схеми даних

---

## Airflow

Проєкт містить **веб-адмінку Airflow**, яка дозволяє:

* Переглядати виконання DAG-ів
* Запускати DAG-и вручну
* Переглядати логи тасків
* Керувати змінними та підключеннями

Airflow автоматично ініціалізується під час першого запуску проєкту.

В браузері:

```
http://localhost:8080
```

Облікові дані:

* Username: `admin`
* Password: `admin`

### Виконання DAG

DAG `nbu_rates` налаштований:

* `schedule_interval = "@daily"`
* `start_date = 2026-01-01`
* `catchup = true`

Це означає:

* Запуски DAG створюються автоматично Airflow Scheduler-ом
* Пропущені запуску з `start_date` будуть виконані
* Ручний запуск через UI — опціонально

---

## Покроковий запуск

### 1. Підготовка середовища та запуск контейнерів

```bash
make up
```

* Якщо `.env` не існує, команда автоматично:

  * Виконає `make init` (створить `.env` і `docker-compose.yml`)
  * Ініціалізує Airflow (БД + admin user)
  * Застосує міграції ClickHouse
  * Підніме всі Docker-контейнери у фоні

---

### 2. Перевірка даних

```bash
make check-rates
```

* Перевіряємо, що дані успішно збережені

---

### 3. Зупинка або очищення проєкту

**Зупинити контейнери (дані зберігаються):**

```bash
make stop
```

**Повне видалення контейнерів і даних:**

```bash
make destroy
```

---

## Опис команд

### Перший запуск (виконується лише один раз)

```bash
make init
```

Команда виконує повну початкову ініціалізацію:

1. Копіює Docker Compose конфігурацію для dev-середовища
2. Копіює dev-змінні середовища у `.env`

---

### Ініціалізація Airflow (технічна команда)

```bash
make airflow-init
```

Використовується всередині `make init`:

* Оновлює БД Airflow
* Створює адміністратора Airflow з даних у `.env`

---

### Міграції ClickHouse

```bash
make migrate-up
```

* Виконує всі SQL-скрипти з `src/migrations/clickhouse/`
* Створює або оновлює структуру таблиць у ClickHouse

---

### Керування Python-залежностями

```bash
make poentry CMD="add requests"
```

* Запускає команди Poetry всередині контейнера Airflow
* Використовується для додавання або оновлення бібліотек

---

### Перевірка даних у ClickHouse

```bash
make check-rates
```

* Виконує SQL-запит до ClickHouse
* Виводить збережені курси валют у консоль

---

### Повне очищення проєкту

```bash
make destroy
```

* Зупиняє всі контейнери
* Видаляє volumes, images та orphan-контейнери
* Повністю очищає стан проєкту

---

## Конфігурація

Усі змінні середовища зберігаються у файлі `.env`, зокрема:

* Облікові дані Airflow
* Параметри підключення до ClickHouse
* Сервісні налаштування

---

## Примітки

* Наразі підтримується лише **dev**-середовище
* Проєкт призначений для локальної розробки та тестування

## TL;DR

```text
make up 
make check-rates
make stop | make destroy
```