# Redis Performance Analysis Project (4411-redis)

## Overview
This repository contains the code and resources for a performance analysis project focusing on Redis, an in-memory data store, in comparison with PostgreSQL, a traditional relational database management system. The project demonstrates the strengths and weaknesses of each system in handling specific data operations.

## Motivation
The motivation behind this project is to understand the performance trade-offs between using an in-memory database like Redis and a traditional disk-based database like PostgreSQL, particularly in the context of high-volume data operations common in real-time analytics and web applications.

## Authors
- [Author 1 Name]
- [Author 2 Name]

## Repository Structure

- `games_details_202312161309.csv`: The dataset file containing details about various games.
- `script.sql`: A SQL script for setting up the PostgreSQL database schema and initial data.
- `requirements.txt`: A list of Python dependencies required to run the Python script.
- `4411_redis_test.py`: The main Python script that performs performance tests comparing Redis and PostgreSQL.
- `README.md`: This file, providing an overview and instructions for running the project.

## Installation and Setup

### Prerequisites
- PostgreSQL: [Installation Guide](https://www.postgresql.org/download/)
- Redis: [Installation Guide](https://redis.io/download)

### Setting Up the Database
1. Install PostgreSQL and ensure it is running on your machine.
2. Run the following command to set up the database using `script.sql`:
   ```
   psql -U <username> -f script.sql
   ```
Replace `<username>` with your PostgreSQL username.

### Installing Python Dependencies
1. Ensure Python is installed on your machine.
2. Install the required Python libraries by running:

```
pip install -r requirements.txt
```

## Running the Tests
To run the performance tests and compare Redis with PostgreSQL, execute the Python script using:

```
python 4411_redis_test.py
```

This script will perform a series of data insertions and retrievals on both Redis and PostgreSQL and output the average durations of these operations.


The script conducts a series of data insertions and retrievals in both Redis and PostgreSQL, then reports the average time taken for these operations.

## Expected Results

- **Redis Performance**: Redis is expected to perform data operations more quickly, demonstrating its efficiency with high-speed, in-memory data processing.
- **PostgreSQL Performance**: Typically, PostgreSQL will show slower operation times in comparison to Redis, which is consistent with the expected performance of disk-based relational databases.
- **Relative Comparison**: The script’s results should hopefully highlight the notable differences in speed between Redis and PostgreSQL, underscoring Redis's faster data handling capabilities in certain situations.
