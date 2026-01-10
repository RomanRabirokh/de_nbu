CREATE DATABASE IF NOT EXISTS nbu;

CREATE TABLE IF NOT EXISTS nbu.rates (
    id String, 
    currency String,
    rate Float64,
    date Date,
    updated_at DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY (currency, date);
