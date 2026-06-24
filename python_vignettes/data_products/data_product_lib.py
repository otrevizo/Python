"""
Data Product library — reusable classes for metadata, semantic layer,
lineage tracking, and DataProduct wrapping.

Designed for use across vignettes that demonstrate data product properties
(discoverability, self-description, quality governance, lineage).
"""
from dataclasses import dataclass
from datetime import datetime
import json
import pandas as pd


@dataclass
class DataProductMetadata:
    name: str
    description: str
    domain: str
    owner: str
    source: str
    source_url: str
    license: str
    version: str
    refresh_frequency: str
    created_at: str  # ISO timestamp


class SemanticLayer:
    """Registry mapping business-friendly names to underlying columns."""

    def __init__(self):
        self._registry: dict[str, dict] = {}

    def register(self, name: str, column: str, unit: str,
                 description: str, source_system: str = None) -> None:
        self._registry[name] = {
            'column':        column,
            'unit':          unit,
            'description':   description,
            'source_system': source_system,
        }

    def get(self, name: str) -> dict:
        return self._registry[name]

    def to_dict(self) -> dict:
        return dict(self._registry)


class LineageTracker:
    """Append-only log of pipeline steps."""

    def __init__(self):
        self._log: list[dict] = []

    def log(self, step: str, operation: str,
            input_shape: tuple, output_shape: tuple,
            notes: str = None) -> None:
        self._log.append({
            'step':         step,
            'operation':    operation,
            'input_shape':  input_shape,
            'output_shape': output_shape,
            'notes':        notes,
            'timestamp':    datetime.utcnow().isoformat(),
        })

    def to_list(self) -> list[dict]:
        return list(self._log)


class DataProduct:
    """Wraps a DataFrame with metadata, semantic layer, and lineage."""

    def __init__(self, data: pd.DataFrame,
                 metadata: DataProductMetadata,
                 semantic_layer: SemanticLayer = None,
                 lineage: LineageTracker = None):
        self.data           = data
        self.metadata       = metadata
        self.semantic_layer = semantic_layer or SemanticLayer()
        self.lineage        = lineage or LineageTracker()

    def schema(self) -> dict:
        """Inferred dtypes per column."""
        return {col: str(dtype) for col, dtype in self.data.dtypes.items()}

    def quality(self) -> dict:
        """Completeness %, row count, column count, freshness."""
        total = len(self.data)
        completeness = {
            col: round(self.data[col].notna().sum() / total * 100, 2)
            for col in self.data.columns
        }
        return {
            'row_count':       total,
            'column_count':    len(self.data.columns),
            'completeness_pct': completeness,
            'freshness':       self.metadata.created_at,
        }

    def card(self) -> None:
        """Pretty-print a human-readable data product summary."""
        q = self.quality()
        sep = '=' * 62
        print(sep)
        print(f"  Data Product : {self.metadata.name}")
        print(sep)
        print(f"  Description  : {self.metadata.description}")
        print(f"  Domain       : {self.metadata.domain}")
        print(f"  Owner        : {self.metadata.owner}")
        print(f"  Source       : {self.metadata.source}")
        print(f"  License      : {self.metadata.license}")
        print(f"  Version      : {self.metadata.version}")
        print(f"  Refresh      : {self.metadata.refresh_frequency}")
        print(f"  Created      : {self.metadata.created_at}")
        print(f"  Rows         : {q['row_count']:,}")
        print(f"  Columns      : {q['column_count']}")
        print(sep)
        entries = self.semantic_layer.to_dict()
        print(f"  Semantic layer ({len(entries)} entries):")
        for name, entry in entries.items():
            print(f"    {name:30s} → {entry['column']}  [{entry['unit']}]")
        print(sep)
        low = {c: v for c, v in q['completeness_pct'].items() if v < 100}
        if low:
            print("  Incomplete columns (<100%):")
            for c, v in low.items():
                print(f"    {c:42s} {v:.1f}%")
        else:
            print("  All columns 100% complete.")
        print(sep)
        steps = self.lineage.to_list()
        print(f"  Lineage ({len(steps)} steps):")
        for s in steps:
            note = f"  // {s['notes']}" if s['notes'] else ''
            print(f"    [{s['step']}] {s['operation']}"
                  f"  {s['input_shape']} → {s['output_shape']}{note}")
        print(sep)

    def contract(self, path: str) -> None:
        """Write JSON sidecar: schema + semantic layer + quality + lineage."""
        payload = {
            'metadata':      {
                'name':             self.metadata.name,
                'description':      self.metadata.description,
                'domain':           self.metadata.domain,
                'owner':            self.metadata.owner,
                'source':           self.metadata.source,
                'source_url':       self.metadata.source_url,
                'license':          self.metadata.license,
                'version':          self.metadata.version,
                'refresh_frequency': self.metadata.refresh_frequency,
                'created_at':       self.metadata.created_at,
            },
            'schema':        self.schema(),
            'semantic_layer': self.semantic_layer.to_dict(),
            'quality':        self.quality(),
            'lineage':        self.lineage.to_list(),
        }
        with open(path, 'w') as f:
            json.dump(payload, f, indent=2)
        print(f"Contract written: {path}")
