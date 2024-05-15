from pathlib import Path

from solar_registry.service.cos_sync import CosSyncService


def test_sync_meta_data():
    workdir = str(
        (Path(__file__).parent / "testdata" / "stable_index_file_check").resolve()
    )

    cos_sync = CosSyncService(workdir)
    cos_sync.sync_meta_data()
