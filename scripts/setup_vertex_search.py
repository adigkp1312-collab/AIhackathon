"""
Set up Vertex AI Search datastore and import course data.

Prerequisites:
    - GCP project with Discovery Engine API enabled
    - gcloud auth application-default login
    - Run scrape_courses.py first to generate data/ai_courses.jsonl

Usage:
    python scripts/setup_vertex_search.py
"""

import os
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "ai_courses.jsonl"

GCP_PROJECT = os.getenv("GCP_PROJECT_ID", "project-9881b278-0a45-47c1-9ed")
LOCATION = "global"
DATASTORE_ID = "ai-education-courses"
ENGINE_ID = "ai_education_engine"


def setup_datastore():
    """Create Vertex AI Search datastore and engine via Discovery Engine API."""
    try:
        from google.cloud import discoveryengine_v1 as discoveryengine
    except ImportError:
        print("[SETUP] Install: pip install google-cloud-discoveryengine")
        print("[SETUP] Falling back to gcloud CLI instructions...\n")
        print_gcloud_instructions()
        return

    # 1. Create DataStore
    client = discoveryengine.DataStoreServiceClient()
    parent = f"projects/{GCP_PROJECT}/locations/{LOCATION}/collections/default_collection"

    try:
        datastore = discoveryengine.DataStore(
            display_name="AI Education Courses",
            industry_vertical=discoveryengine.IndustryVertical.GENERIC,
            solution_types=[discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH],
            content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED,
        )

        operation = client.create_data_store(
            parent=parent,
            data_store=datastore,
            data_store_id=DATASTORE_ID,
        )
        print(f"[SETUP] Creating datastore... {operation.operation.name}")
        result = operation.result(timeout=300)
        print(f"[SETUP] Datastore created: {result.name}")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"[SETUP] Datastore already exists: {DATASTORE_ID}")
        else:
            print(f"[SETUP] Datastore creation error: {e}")

    # 2. Create Engine
    engine_client = discoveryengine.EngineServiceClient()
    try:
        engine = discoveryengine.Engine(
            display_name="AI Education Search Engine",
            solution_type=discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH,
            search_engine_config=discoveryengine.Engine.SearchEngineConfig(
                search_tier=discoveryengine.SearchTier.SEARCH_TIER_STANDARD,
            ),
            data_store_ids=[DATASTORE_ID],
        )

        operation = engine_client.create_engine(
            parent=parent,
            engine=engine,
            engine_id=ENGINE_ID,
        )
        print(f"[SETUP] Creating engine... {operation.operation.name}")
        result = operation.result(timeout=300)
        print(f"[SETUP] Engine created: {result.name}")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"[SETUP] Engine already exists: {ENGINE_ID}")
        else:
            print(f"[SETUP] Engine creation error: {e}")

    # 3. Import documents
    import_documents()


def import_documents():
    """Import JSONL course data into the datastore."""
    if not DATA_FILE.exists():
        print(f"[SETUP] Data file not found: {DATA_FILE}")
        print("[SETUP] Run: python scripts/scrape_courses.py first")
        return

    try:
        from google.cloud import discoveryengine_v1 as discoveryengine

        client = discoveryengine.DocumentServiceClient()
        parent = (
            f"projects/{GCP_PROJECT}/locations/{LOCATION}"
            f"/collections/default_collection/dataStores/{DATASTORE_ID}"
            f"/branches/default_branch"
        )

        with open(DATA_FILE) as f:
            for line in f:
                course = json.loads(line.strip())
                doc_id = course.get("id", course["url"].split("/")[-1][:63])

                doc = discoveryengine.Document(
                    id=doc_id,
                    json_data=json.dumps(course),
                    name=f"{parent}/documents/{doc_id}",
                )

                try:
                    client.create_document(
                        parent=parent,
                        document=doc,
                        document_id=doc_id,
                    )
                    print(f"  [DOC] Created: {course['title'][:50]}")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        client.update_document(document=doc)
                        print(f"  [DOC] Updated: {course['title'][:50]}")
                    else:
                        print(f"  [DOC] Error: {e}")

        print("[SETUP] Document import complete.")
    except ImportError:
        print("[SETUP] google-cloud-discoveryengine not installed.")


def print_gcloud_instructions():
    """Print manual gcloud setup commands."""
    print(f"""
Manual setup using gcloud CLI:

# 1. Enable Discovery Engine API
gcloud services enable discoveryengine.googleapis.com --project={GCP_PROJECT}

# 2. Create datastore (via console)
# Go to: https://console.cloud.google.com/gen-app-builder/data-stores
# Create a new datastore with:
#   - Name: AI Education Courses
#   - Type: Unstructured with metadata
#   - Import: Upload {DATA_FILE}

# 3. Create search app/engine
# Go to: https://console.cloud.google.com/gen-app-builder/engines
# Create a new search app with:
#   - Name: AI Education Search Engine
#   - Data store: AI Education Courses

# Engine path will be:
# projects/{GCP_PROJECT}/locations/global/collections/default_collection/engines/{ENGINE_ID}
""")


if __name__ == "__main__":
    setup_datastore()
