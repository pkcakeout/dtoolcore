"""Test the DiskStorageBroker self description metadata."""

import os
import json

from . import tmp_dir_fixture  # NOQA


def test_writing_of_dtool_structure_file(tmp_dir_fixture):  # NOQA

    from dtoolcore import generate_admin_metadata, generate_proto_dataset

    name = "my_dataset"
    admin_metadata = generate_admin_metadata(name)
    proto_dataset = generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=tmp_dir_fixture,
        config_path=None
    )
    proto_dataset.create()
    proto_dataset.freeze()

    expected_dtool_structure_fpath = os.path.join(
        tmp_dir_fixture,
        name,
        ".dtool",
        "structure.json"
    )
    assert os.path.isfile(expected_dtool_structure_fpath)

    expected_content = {
        "data_directory": ["data"],
        "dataset_readme_relpath": ["README.yml"],
        "dtool_directory": [".dtool"],
        "admin_metadata_relpath": [".dtool", "dtool"],
        "structure_metadata_relpath": [".dtool", "structure.json"],
        "dtool_readme_relpath": [".dtool", "README.txt"],
        "manifest_relpath": [".dtool", "manifest.json"],
        "overlays_directory": [".dtool", "overlays"],
        "metadata_fragments_directory": [".dtool", "tmp_fragments"],
    }

    with open(expected_dtool_structure_fpath) as fh:
        actual_content = json.load(fh)
    assert expected_content == actual_content


def test_writing_of_dtool_readme_file(tmp_dir_fixture):  # NOQA

    from dtoolcore import generate_admin_metadata, generate_proto_dataset

    name = "my_dataset"
    admin_metadata = generate_admin_metadata(name)
    proto_dataset = generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=tmp_dir_fixture,
        config_path=None
    )
    proto_dataset.create()
    proto_dataset.freeze()

    expected_dtool_structure_fpath = os.path.join(
        tmp_dir_fixture,
        name,
        ".dtool",
        "README.txt"
    )
    assert os.path.isfile(expected_dtool_structure_fpath)

    with open(expected_dtool_structure_fpath) as fh:
        actual_content = fh.read()
    assert actual_content.startswith("README")
