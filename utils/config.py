import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists(os.path.join(PROJECT_ROOT, "datasets")):
    os.makedirs(os.path.join(PROJECT_ROOT, "datasets"))

if not os.path.exists(os.path.join(PROJECT_ROOT, "datasets", "parquet")):
    os.makedirs(os.path.join(PROJECT_ROOT, "datasets", "parquet"))

if not os.path.exists(os.path.join(PROJECT_ROOT, "datasets", "samples")):
    os.makedirs(os.path.join(PROJECT_ROOT, "datasets", "samples"))

if not os.path.exists(os.path.join(PROJECT_ROOT, "features")):
    os.makedirs(os.path.join(PROJECT_ROOT, "features"))
