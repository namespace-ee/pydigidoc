"""Basic tests for pydigidoc bindings."""

import pydigidoc


class TestImports:
    def test_import_package(self):
        assert pydigidoc is not None

    def test_version_string(self):
        assert isinstance(pydigidoc.__version__, str)
        assert pydigidoc.__version__

    def test_library_version(self):
        v = pydigidoc.version()
        assert isinstance(v, str)
        assert v

    def test_all_public_symbols(self):
        for name in pydigidoc.__all__:
            assert hasattr(pydigidoc, name), f"Missing symbol: {name}"


class TestContainer:
    def test_container_class(self):
        assert pydigidoc.Container is not None

    def test_container_open_cb(self):
        assert pydigidoc.ContainerOpenCB is not None


class TestSigners:
    def test_pkcs11_signer_class(self):
        assert pydigidoc.PKCS11Signer is not None

    def test_pkcs12_signer_class(self):
        assert pydigidoc.PKCS12Signer is not None

    def test_external_signer_class(self):
        assert pydigidoc.ExternalSigner is not None


class TestConfiguration:
    def test_conf_class(self):
        assert pydigidoc.Conf is not None

    def test_digidoc_conf_class(self):
        assert pydigidoc.DigiDocConf is not None


class TestContainerTypes:
    def test_string_vector(self):
        sv = pydigidoc.StringVector()
        sv.append("hello")
        sv.append("world")
        assert len(sv) == 2
        assert sv[0] == "hello"
        assert sv[1] == "world"

    def test_string_map(self):
        sm = pydigidoc.StringMap()
        sm["key"] = "value"
        assert sm["key"] == "value"

    def test_data_files_vector(self):
        df = pydigidoc.DataFiles()
        assert len(df) == 0

    def test_signatures_vector(self):
        sigs = pydigidoc.Signatures()
        assert len(sigs) == 0


class TestIntegration:
    """Tests that require initialize() — create/open containers."""

    def test_create_container(self, lib, tmp_path):
        path = str(tmp_path / "test.asice")
        doc = pydigidoc.Container.create(path)
        assert doc is not None
        del doc

    def test_create_add_datafile_save(self, lib, tmp_path):
        # Create a data file to add
        data_file = tmp_path / "hello.txt"
        data_file.write_text("Hello, world!")

        path = str(tmp_path / "test.asice")
        doc = pydigidoc.Container.create(path)
        doc.add_data_file(str(data_file), "text/plain")
        assert len(doc.data_files()) == 1

        df = doc.data_files()[0]
        assert df.file_name() == "hello.txt"
        assert df.media_type() == "text/plain"
        assert df.file_size() == 13

        doc.save()
        del doc

        # Reopen and verify
        doc2 = pydigidoc.Container.open(path)
        assert len(doc2.data_files()) == 1
        assert doc2.data_files()[0].file_name() == "hello.txt"
        del doc2

    def test_create_remove_datafile(self, lib, tmp_path):
        data_file = tmp_path / "hello.txt"
        data_file.write_text("Hello")

        path = str(tmp_path / "test.asice")
        doc = pydigidoc.Container.create(path)
        doc.add_data_file(str(data_file), "text/plain")
        assert len(doc.data_files()) == 1

        doc.remove_data_file(0)
        assert len(doc.data_files()) == 0
        del doc

    def test_container_open_cb_subclass(self, lib, tmp_path):
        """Test that ContainerOpenCB can be subclassed from Python (director)."""

        class MyCallback(pydigidoc.ContainerOpenCB):
            def __init__(self):
                super().__init__()
                self.called = False

            def validate_online(self):
                self.called = True
                return False

        data_file = tmp_path / "hello.txt"
        data_file.write_text("Hello")

        path = str(tmp_path / "test.asice")
        doc = pydigidoc.Container.create(path)
        doc.add_data_file(str(data_file), "text/plain")
        doc.save()
        del doc

        cb = MyCallback()
        doc2 = pydigidoc.Container.open(path, cb)
        assert doc2 is not None
        del doc2

    def test_app_info(self, lib):
        info = pydigidoc.app_info()
        assert isinstance(info, str)
        assert "pydigidoc-test" in info

    def test_user_agent(self, lib):
        ua = pydigidoc.user_agent()
        assert isinstance(ua, str)
        assert ua

    def test_initialize_lib_custom_path(self, tmp_path):
        """Test initialize_lib() with a custom schema directory."""
        schema_dir = pydigidoc._SCHEMA_DIR
        pydigidoc.initialize_lib("pydigidoc-test-custom", schema_dir)
        try:
            info = pydigidoc.app_info()
            assert "pydigidoc-test-custom" in info
        finally:
            pydigidoc.terminate()
