from base64 import b64decode, b64encode
from ariadne import ScalarType


def newBase64Scalar() -> ScalarType:
    base64_scalar = ScalarType('Base64')
    @base64_scalar.serializer
    def serialize_base64(v):
        return str(b64encode(v), 'UTF-8')

    @base64_scalar.value_parser
    def parse_base64_value(v):
        return b64decode(v.encode('UTF-8'))
    return base64_scalar