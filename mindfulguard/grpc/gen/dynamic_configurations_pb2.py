# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dynamic_configurations.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x64ynamic_configurations.proto\x12\x16\x64ynamic_configurations\"(\n\nPutRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\"C\n\x0bPutResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12!\n\x19\x65xecutionTimeMilliseconds\x18\x02 \x01(\x03\"\x19\n\nGetRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"R\n\x0bGetResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12!\n\x19\x65xecutionTimeMilliseconds\x18\x02 \x01(\x03\x12\r\n\x05value\x18\x03 \x01(\x0c\" \n\x0eGetListRequest\x12\x0e\n\x06prefix\x18\x01 \x01(\t\"U\n\x0fGetListResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12!\n\x19\x65xecutionTimeMilliseconds\x18\x02 \x01(\x03\x12\x0c\n\x04list\x18\x03 \x03(\t\"\x1c\n\rDeleteRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"F\n\x0e\x44\x65leteResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12!\n\x19\x65xecutionTimeMilliseconds\x18\x02 \x01(\x03\"#\n\x11\x44\x65leteTreeRequest\x12\x0e\n\x06prefix\x18\x01 \x01(\t\"[\n\x12\x44\x65leteTreeResponse\x12\x11\n\ttimestamp\x18\x01 \x01(\t\x12!\n\x19\x65xecutionTimeMilliseconds\x18\x02 \x01(\x03\x12\x0f\n\x07\x64\x65leted\x18\x03 \x01(\x05\x32\xdb\x03\n\x15\x44ynamicConfigurations\x12P\n\x03Put\x12\".dynamic_configurations.PutRequest\x1a#.dynamic_configurations.PutResponse\"\x00\x12P\n\x03Get\x12\".dynamic_configurations.GetRequest\x1a#.dynamic_configurations.GetResponse\"\x00\x12\\\n\x07GetList\x12&.dynamic_configurations.GetListRequest\x1a\'.dynamic_configurations.GetListResponse\"\x00\x12Y\n\x06\x44\x65lete\x12%.dynamic_configurations.DeleteRequest\x1a&.dynamic_configurations.DeleteResponse\"\x00\x12\x65\n\nDeleteTree\x12).dynamic_configurations.DeleteTreeRequest\x1a*.dynamic_configurations.DeleteTreeResponse\"\x00\x42\x1eZ\x1c\x64ynamic_configurations.v1;v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dynamic_configurations_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\034dynamic_configurations.v1;v1'
  _globals['_PUTREQUEST']._serialized_start=56
  _globals['_PUTREQUEST']._serialized_end=96
  _globals['_PUTRESPONSE']._serialized_start=98
  _globals['_PUTRESPONSE']._serialized_end=165
  _globals['_GETREQUEST']._serialized_start=167
  _globals['_GETREQUEST']._serialized_end=192
  _globals['_GETRESPONSE']._serialized_start=194
  _globals['_GETRESPONSE']._serialized_end=276
  _globals['_GETLISTREQUEST']._serialized_start=278
  _globals['_GETLISTREQUEST']._serialized_end=310
  _globals['_GETLISTRESPONSE']._serialized_start=312
  _globals['_GETLISTRESPONSE']._serialized_end=397
  _globals['_DELETEREQUEST']._serialized_start=399
  _globals['_DELETEREQUEST']._serialized_end=427
  _globals['_DELETERESPONSE']._serialized_start=429
  _globals['_DELETERESPONSE']._serialized_end=499
  _globals['_DELETETREEREQUEST']._serialized_start=501
  _globals['_DELETETREEREQUEST']._serialized_end=536
  _globals['_DELETETREERESPONSE']._serialized_start=538
  _globals['_DELETETREERESPONSE']._serialized_end=629
  _globals['_DYNAMICCONFIGURATIONS']._serialized_start=632
  _globals['_DYNAMICCONFIGURATIONS']._serialized_end=1107
# @@protoc_insertion_point(module_scope)