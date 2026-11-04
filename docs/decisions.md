# Decision Log

Each entry records a design decision, the context behind it, and its consequences. New decisions are added at the bottom; superseded ones are marked, not deleted.

---

## ADR-001: Use the CFPB Consumer Complaint Database

**Context:** The project needs a large, regularly updated dataset with free text for an AI stage, ideally in financial services.
**Decision:** Use the CFPB data: the narratives archive for history and the API for daily updates.
**Consequences:** Narrative publication stopped on 14 August 2026, so the RAG corpus is fixed while structured data keeps updating. The two sources must be conformed.

---

## ADR-002: Snowflake as the warehouse

**Context:** Options were Snowflake, BigQuery and Postgres.
**Decision:** Snowflake.
**Consequences:** Strong demand in the target job market; native `VECTOR` type keeps embeddings next to the star schema. Ongoing cost after the trial, controlled with auto-suspend.

---

## ADR-003: S3 as the data lake

**Context:** Snowflake internal stages could hold files, removing the need for S3.
**Decision:** Use S3 for the bronze and silver layers.
**Consequences:** Spark writes to a neutral location any engine can read; the warehouse can be rebuilt or replaced without reprocessing. Adds one service to manage.

---

## ADR-004: Run PySpark locally in Docker

**Context:** Spark could run on Databricks or locally.
**Decision:** Local Spark in Docker, orchestrated by Airflow.
**Consequences:** Fully reproducible with `docker compose up`. Volume is limited by the local machine, so the design is documented as cluster-ready rather than claimed as large-scale.

---

## ADR-005: EtLT transformation pattern

**Context:** Transformations could all live in Spark (ETL) or all in dbt (ELT).
**Decision:** Technical conforming in Spark before loading; all business logic in dbt.
**Consequences:** Clean, warehouse-independent silver layer. Two places hold transformation code, so the boundary (no business logic in Spark) must be kept.

---

## ADR-006: Kimball dimensional modelling

**Context:** Alternatives were an Inmon 3NF warehouse or Data Vault.
**Decision:** Kimball star schema.
**Consequences:** Fits a single subject area and analytical queries; maps cleanly onto dbt layers. Would need revisiting if many more source systems were added.

---

## ADR-007: Accumulating snapshot fact built from a dbt snapshot

**Context:** Complaint responses change after first publication, and the question "how long do companies take to close complaints?" needs that history.
**Decision:** A dbt snapshot records each version of each complaint; `fct_complaints` is an accumulating snapshot fact with milestone dates derived from it.
**Consequences:** Daily precision only; no history before the first snapshot run. The snapshot cannot be rebuilt and must be protected.

---

## ADR-008: RAG rather than ML features for the AI stage

**Context:** The AI stage could produce features for a predictive model or embeddings for retrieval.
**Decision:** RAG over complaint narratives.
**Consequences:** Demonstrates data engineering for AI (chunking, embeddings, incremental processing, evaluation) rather than model building, matching the target roles.

---

## ADR-009: Plain Parquet now, Iceberg later

**Context:** The silver layer could use Apache Iceberg for an open lakehouse.
**Decision:** Start with plain partitioned Parquet; consider Iceberg once the pipeline works end to end.
**Consequences:** Simpler first build; Iceberg stays a planned enhancement.

---

## ADR-010: Local open-source embedding model

**Context:** Embeddings could come from a paid API or a local model.
**Decision:** A local sentence-transformer model, starting with a subset of narratives.
**Consequences:** No per-call cost; slower on CPU. The model name is stored with each embedding so a future model change can be tracked and re-run.
