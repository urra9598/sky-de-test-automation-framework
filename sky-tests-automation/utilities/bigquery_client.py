"""Small BigQuery helper wrapper for the framework.

This module provides a lightweight wrapper around google-cloud-bigquery to:
- create a client from a service account file or default credentials
- run queries and return results as list[dict] or pandas.DataFrame (if available)
- load a pandas DataFrame to a BigQuery table

Usage:
    from utilities.bigquery_client import BigQueryClient, client_from_config

    # Create manually
    bq = BigQueryClient(project='my-project', credentials_path='/path/to/key.json')
    rows = bq.query('SELECT 1 as v')

    # Or use config-driven helper (reads config.bigquery)
    bq = client_from_config()
    df = bq.query('SELECT * FROM dataset.table', as_dataframe=True)

Configuration (example in `sky-tests-automation/config/bigquery.config.json`):
{
  "project": "my-gcp-project",
  "credentials_file": "/abs/path/to/service-account.json",
  "use_default_credentials": false
}
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

LOG = logging.getLogger(__name__)


class BigQueryClient:
    def __init__(
        self,
        project: Optional[str] = None,
        credentials_path: Optional[Union[str, Path]] = None,
        use_default_credentials: bool = False,
    ):
        """Create a BigQuery client wrapper.

        - If `credentials_path` is provided, the client is created from that service
          account JSON file.
        - If `use_default_credentials` is True (or credentials_path is None and
          use_default_credentials True), it uses ADC (Application Default Credentials).
        - `project` can be provided to override the client project.
        """
        try:
            from google.cloud import bigquery
            from google.oauth2 import service_account
        except Exception as e:  # pragma: no cover - runtime dependency
            raise RuntimeError(
                "google-cloud-bigquery is required. Install with `pip install google-cloud-bigquery`."
            ) from e

        self._bq = bigquery
        self._client = None

        if credentials_path and not use_default_credentials:
            cred_path = Path(credentials_path).expanduser().resolve()
            if not cred_path.exists():
                raise FileNotFoundError(f"BigQuery credentials file not found: {cred_path}")
            creds = service_account.Credentials.from_service_account_file(str(cred_path))
            self._client = bigquery.Client(project=project or creds.project_id, credentials=creds)
        else:
            # Use application default credentials
            self._client = bigquery.Client(project=project)

    @property
    def client(self):
        return self._client

    def query(self, sql: str, params: Optional[Iterable[Any]] = None, as_dataframe: bool = False, **kwargs):
        """Run a SQL query and return results.

        - If `as_dataframe=True` and pandas is available, returns a `pandas.DataFrame`.
        - Otherwise returns a list of dicts (rows).
        Additional kwargs are forwarded to `client.query()`.
        """
        job = self._client.query(sql, job_config=kwargs.get("job_config"))
        result = job.result()

        if as_dataframe:
            try:
                import pandas as pd

                df = result.to_dataframe()
                return df
            except Exception:
                LOG.exception("pandas unavailable or conversion failed; falling back to list of dicts")

        rows = [dict(r) for r in result]
        return rows

    def load_dataframe(
        self,
        df,  # pandas.DataFrame
        destination: str,
        write_disposition: str = "WRITE_TRUNCATE",
        chunk_size: Optional[int] = None,
        job_config: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Load a pandas DataFrame into a BigQuery table.

        - `destination` is a table id: `project.dataset.table` or `dataset.table`.
        - Returns job.result() information summary as a dict.
        """
        try:
            from google.cloud import bigquery
        except Exception:  # pragma: no cover
            raise RuntimeError("google-cloud-bigquery is required for load operations")

        if job_config is None:
            job_config = bigquery.LoadJobConfig()
            job_config.write_disposition = getattr(bigquery.WriteDisposition, write_disposition, write_disposition)

        job = self._client.load_table_from_dataframe(df, destination, job_config=job_config)
        res = job.result()
        return {"destination": destination, "output_rows": res.output_rows}

    def insert_rows_json(self, table: str, json_rows: Iterable[Dict[str, Any]]):
        """Insert JSON rows into a table using client.insert_rows_json.

        Returns the API response (empty list on success).
        """
        errors = self._client.insert_rows_json(table, list(json_rows))
        if errors:
            LOG.error("Errors inserting rows into %s: %s", table, errors)
        return errors


def client_from_config(config: Optional[Dict[str, Any]] = None) -> BigQueryClient:
    """Create a BigQueryClient using the framework ConfigManager configuration.

    If `config` dict is provided it will be used; otherwise the function will try
    to read from `utilities.config_manager.config` and the `bigquery` section.
    """
    if config is None:
        try:
            from utilities.config_manager import config as CFG

            config = CFG.get_all().get("bigquery", {})
        except Exception:
            config = {}

    project = config.get("project")
    credentials_file = config.get("credentials_file")
    use_default = bool(config.get("use_default_credentials", False))

    return BigQueryClient(project=project, credentials_path=credentials_file, use_default_credentials=use_default)
