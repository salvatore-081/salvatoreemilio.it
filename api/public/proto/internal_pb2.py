# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: internal.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='internal.proto',
  package='internal',
  syntax='proto3',
  serialized_options=b'ZWhttps://github.com/salvatore-081/salvatoreemilio.it/tree/development/api/internal/proto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0einternal.proto\x12\x08internal\"\x1d\n\x0cGetUserInput\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"b\n\x04User\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07surname\x18\x03 \x01(\t\x12\x13\n\x0bphoneNumber\x18\x04 \x01(\t\x12\x17\n\x0f\x63urrentLocation\x18\x05 \x01(\t\"j\n\x0c\x41\x64\x64UserInput\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07surname\x18\x03 \x01(\t\x12\x13\n\x0bphoneNumber\x18\x04 \x01(\t\x12\x17\n\x0f\x63urrentLocation\x18\x05 \x01(\t\"e\n\x16UpdateUserInputPayload\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07surname\x18\x02 \x01(\t\x12\x13\n\x0bphoneNumber\x18\x03 \x01(\t\x12\x17\n\x0f\x63urrentLocation\x18\x04 \x01(\t\"b\n\x0fUpdateUserInput\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12@\n\x16updateUserInputPayload\x18\x02 \x01(\x0b\x32 .internal.UpdateUserInputPayload\"\x1f\n\x0eWatchUserInput\x12\r\n\x05\x65mail\x18\x01 \x01(\t2\xea\x01\n\x08Internal\x12\x33\n\x07GetUser\x12\x16.internal.GetUserInput\x1a\x0e.internal.User\"\x00\x12\x33\n\x07\x41\x64\x64User\x12\x16.internal.AddUserInput\x1a\x0e.internal.User\"\x00\x12\x39\n\nUpdateUser\x12\x19.internal.UpdateUserInput\x1a\x0e.internal.User\"\x00\x12\x39\n\tWatchUser\x12\x18.internal.WatchUserInput\x1a\x0e.internal.User\"\x00\x30\x01\x42YZWhttps://github.com/salvatore-081/salvatoreemilio.it/tree/development/api/internal/protob\x06proto3'
)




_GETUSERINPUT = _descriptor.Descriptor(
  name='GetUserInput',
  full_name='internal.GetUserInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='internal.GetUserInput.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=57,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='internal.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='internal.User.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='internal.User.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='surname', full_name='internal.User.surname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='phoneNumber', full_name='internal.User.phoneNumber', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currentLocation', full_name='internal.User.currentLocation', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=157,
)


_ADDUSERINPUT = _descriptor.Descriptor(
  name='AddUserInput',
  full_name='internal.AddUserInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='internal.AddUserInput.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='internal.AddUserInput.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='surname', full_name='internal.AddUserInput.surname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='phoneNumber', full_name='internal.AddUserInput.phoneNumber', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currentLocation', full_name='internal.AddUserInput.currentLocation', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=265,
)


_UPDATEUSERINPUTPAYLOAD = _descriptor.Descriptor(
  name='UpdateUserInputPayload',
  full_name='internal.UpdateUserInputPayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='internal.UpdateUserInputPayload.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='surname', full_name='internal.UpdateUserInputPayload.surname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='phoneNumber', full_name='internal.UpdateUserInputPayload.phoneNumber', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currentLocation', full_name='internal.UpdateUserInputPayload.currentLocation', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=267,
  serialized_end=368,
)


_UPDATEUSERINPUT = _descriptor.Descriptor(
  name='UpdateUserInput',
  full_name='internal.UpdateUserInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='internal.UpdateUserInput.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updateUserInputPayload', full_name='internal.UpdateUserInput.updateUserInputPayload', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=370,
  serialized_end=468,
)


_WATCHUSERINPUT = _descriptor.Descriptor(
  name='WatchUserInput',
  full_name='internal.WatchUserInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='internal.WatchUserInput.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=470,
  serialized_end=501,
)

_UPDATEUSERINPUT.fields_by_name['updateUserInputPayload'].message_type = _UPDATEUSERINPUTPAYLOAD
DESCRIPTOR.message_types_by_name['GetUserInput'] = _GETUSERINPUT
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['AddUserInput'] = _ADDUSERINPUT
DESCRIPTOR.message_types_by_name['UpdateUserInputPayload'] = _UPDATEUSERINPUTPAYLOAD
DESCRIPTOR.message_types_by_name['UpdateUserInput'] = _UPDATEUSERINPUT
DESCRIPTOR.message_types_by_name['WatchUserInput'] = _WATCHUSERINPUT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetUserInput = _reflection.GeneratedProtocolMessageType('GetUserInput', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERINPUT,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:internal.GetUserInput)
  })
_sym_db.RegisterMessage(GetUserInput)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:internal.User)
  })
_sym_db.RegisterMessage(User)

AddUserInput = _reflection.GeneratedProtocolMessageType('AddUserInput', (_message.Message,), {
  'DESCRIPTOR' : _ADDUSERINPUT,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:internal.AddUserInput)
  })
_sym_db.RegisterMessage(AddUserInput)

UpdateUserInputPayload = _reflection.GeneratedProtocolMessageType('UpdateUserInputPayload', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERINPUTPAYLOAD,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:internal.UpdateUserInputPayload)
  })
_sym_db.RegisterMessage(UpdateUserInputPayload)

UpdateUserInput = _reflection.GeneratedProtocolMessageType('UpdateUserInput', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERINPUT,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:internal.UpdateUserInput)
  })
_sym_db.RegisterMessage(UpdateUserInput)

WatchUserInput = _reflection.GeneratedProtocolMessageType('WatchUserInput', (_message.Message,), {
  'DESCRIPTOR' : _WATCHUSERINPUT,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:internal.WatchUserInput)
  })
_sym_db.RegisterMessage(WatchUserInput)


DESCRIPTOR._options = None

_INTERNAL = _descriptor.ServiceDescriptor(
  name='Internal',
  full_name='internal.Internal',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=504,
  serialized_end=738,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetUser',
    full_name='internal.Internal.GetUser',
    index=0,
    containing_service=None,
    input_type=_GETUSERINPUT,
    output_type=_USER,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='AddUser',
    full_name='internal.Internal.AddUser',
    index=1,
    containing_service=None,
    input_type=_ADDUSERINPUT,
    output_type=_USER,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateUser',
    full_name='internal.Internal.UpdateUser',
    index=2,
    containing_service=None,
    input_type=_UPDATEUSERINPUT,
    output_type=_USER,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='WatchUser',
    full_name='internal.Internal.WatchUser',
    index=3,
    containing_service=None,
    input_type=_WATCHUSERINPUT,
    output_type=_USER,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_INTERNAL)

DESCRIPTOR.services_by_name['Internal'] = _INTERNAL

# @@protoc_insertion_point(module_scope)
