create table if not exists {PERSONAL_FINANCES_SCHEMA_NAME}.balance (
    uuid varchar(36) not null,
    run_timestamp varchar(32) not null,
    balance_type varchar not null,
    balance_value float not null
);
