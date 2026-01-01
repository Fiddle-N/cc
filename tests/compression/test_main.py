import io

from cc.compression import main


def test_encode_decode():
    text = "my name is inigo montoya prepare to die"
    input_file = io.BytesIO()
    input_file.write(text.encode("utf-8"))
    input_file.seek(0)
    compressed_file = io.BytesIO()

    main.compress_file(input_file, compressed_file)

    compressed_file.seek(0)
    output_file = io.BytesIO()
    main.decompress_file(compressed_file, output_file)

    assert output_file.getvalue().decode("utf-8") == text
