"""Functional tests for the dtoolcore version 3 .dtool-structure metadata."""

import os
import json
import shutil

from . import tmp_dir_fixture  # NOQA
from . import TEST_SAMPLE_DATA


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
        "readme_relpath": ["README.yml"],
        "dtool_directory": [".dtool"],
        "admin_metadata_relpath": [".dtool", "dtool"],
        "structure_metadata_relpath": [".dtool", "structure.json"],
        "manifest_relpath": [".dtool", "manifest.json"],
        "overlays_directory": [".dtool", "overlays"],
        "metadata_fragments_directory": [".dtool", "tmp_fragments"],
    }
    with open(expected_dtool_structure_fpath) as fh:
        actual_content = json.load(fh)
    assert expected_content == actual_content


def test_reading_of_dtool_structure_file(tmp_dir_fixture):  # NOQA
    from dtoolcore import (
        generate_admin_metadata,
        generate_proto_dataset,
        DataSet,
    )
    from dtoolcore.utils import generate_identifier

    name = "my_dataset"
    admin_metadata = generate_admin_metadata(name)
    proto_dataset = generate_proto_dataset(
        admin_metadata=admin_metadata,
        base_uri=tmp_dir_fixture,
        config_path=None
    )
    proto_dataset.create()

    sample_data_path = os.path.join(TEST_SAMPLE_DATA)
    local_file_path = os.path.join(sample_data_path, 'tiny.png')
    proto_dataset.put_item(local_file_path, 'tiny.png')

    proto_dataset.freeze()

    # Read in the dataset.
    original_dataset = DataSet.from_uri(proto_dataset.uri)
    expected_identifier = generate_identifier('tiny.png')
    assert expected_identifier in original_dataset.identifiers
    assert len(original_dataset.identifiers) == 1

    # Mangle the structure file.
    updated_data_dir_list = ["different_data_dir"]
    dtool_structure_fpath = os.path.join(
        tmp_dir_fixture,
        name,
        ".dtool",
        "structure.json"
    )
    with open(dtool_structure_fpath) as fh:
        structure_content = json.load(fh)
    structure_content["data_directory"] = updated_data_dir_list
    with open(dtool_structure_fpath, "w") as fh:
        json.dump(structure_content, fh)

    # Read in the dataset with the mangled structure file.
    broken_dataset = DataSet.from_uri(proto_dataset.uri)
    generated_manifest = broken_dataset.generate_manifest()
    assert len(generated_manifest["items"]) == 0

    # Mangle the dataset data directory too.
    org_data_dir = os.path.join(
        tmp_dir_fixture,
        name,
        "data",
    )
    new_data_dir = os.path.join(
        tmp_dir_fixture,
        name,
        "different_data_dir",
    )
    shutil.move(org_data_dir, new_data_dir)
    new_dataset = DataSet.from_uri(proto_dataset.uri)
    generated_manifest = new_dataset.generate_manifest()
    assert len(generated_manifest["items"]) == 1

    from dtoolcore.compare import (
        diff_identifiers,
        diff_sizes,
        diff_content
    )
    assert len(diff_identifiers(original_dataset, new_dataset)) == 0
    assert len(diff_sizes(original_dataset, new_dataset)) == 0

    # Need new dataset first otherwise it tries to calculate the hash of
    # the file that has been moved.
    assert len(diff_content(new_dataset, original_dataset)) == 0
