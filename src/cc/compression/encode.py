import io


class Encoder:
    def __init__(self, file: io.BytesIO, pref_code_tbl: dict[str, str]):
        self.file = file
        self.pref_code_tbl = pref_code_tbl

    def _write_header(self):
        pass

    def write(self):
        pass
