"""Functional tests for the dtoolcore version 3 .dtool-structure metadata."""

import os

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
