// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.26.0
// 	protoc        v3.12.4
// source: proto/internal.proto

package proto

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type GetUserInput struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Email string `protobuf:"bytes,1,opt,name=email,proto3" json:"email,omitempty"`
}

func (x *GetUserInput) Reset() {
	*x = GetUserInput{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_internal_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *GetUserInput) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*GetUserInput) ProtoMessage() {}

func (x *GetUserInput) ProtoReflect() protoreflect.Message {
	mi := &file_proto_internal_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use GetUserInput.ProtoReflect.Descriptor instead.
func (*GetUserInput) Descriptor() ([]byte, []int) {
	return file_proto_internal_proto_rawDescGZIP(), []int{0}
}

func (x *GetUserInput) GetEmail() string {
	if x != nil {
		return x.Email
	}
	return ""
}

type User struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Email           string `protobuf:"bytes,1,opt,name=email,proto3" json:"email,omitempty"`
	Name            string `protobuf:"bytes,2,opt,name=name,proto3" json:"name,omitempty"`
	Surname         string `protobuf:"bytes,3,opt,name=surname,proto3" json:"surname,omitempty"`
	PhoneNumber     string `protobuf:"bytes,4,opt,name=phoneNumber,proto3" json:"phoneNumber,omitempty"`
	CurrentLocation string `protobuf:"bytes,5,opt,name=currentLocation,proto3" json:"currentLocation,omitempty"`
}

func (x *User) Reset() {
	*x = User{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_internal_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *User) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*User) ProtoMessage() {}

func (x *User) ProtoReflect() protoreflect.Message {
	mi := &file_proto_internal_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use User.ProtoReflect.Descriptor instead.
func (*User) Descriptor() ([]byte, []int) {
	return file_proto_internal_proto_rawDescGZIP(), []int{1}
}

func (x *User) GetEmail() string {
	if x != nil {
		return x.Email
	}
	return ""
}

func (x *User) GetName() string {
	if x != nil {
		return x.Name
	}
	return ""
}

func (x *User) GetSurname() string {
	if x != nil {
		return x.Surname
	}
	return ""
}

func (x *User) GetPhoneNumber() string {
	if x != nil {
		return x.PhoneNumber
	}
	return ""
}

func (x *User) GetCurrentLocation() string {
	if x != nil {
		return x.CurrentLocation
	}
	return ""
}

type AddUserInput struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Email           string `protobuf:"bytes,1,opt,name=email,proto3" json:"email,omitempty"`
	Name            string `protobuf:"bytes,2,opt,name=name,proto3" json:"name,omitempty"`
	Surname         string `protobuf:"bytes,3,opt,name=surname,proto3" json:"surname,omitempty"`
	PhoneNumber     string `protobuf:"bytes,4,opt,name=phoneNumber,proto3" json:"phoneNumber,omitempty"`
	CurrentLocation string `protobuf:"bytes,5,opt,name=currentLocation,proto3" json:"currentLocation,omitempty"`
}

func (x *AddUserInput) Reset() {
	*x = AddUserInput{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_internal_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *AddUserInput) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*AddUserInput) ProtoMessage() {}

func (x *AddUserInput) ProtoReflect() protoreflect.Message {
	mi := &file_proto_internal_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use AddUserInput.ProtoReflect.Descriptor instead.
func (*AddUserInput) Descriptor() ([]byte, []int) {
	return file_proto_internal_proto_rawDescGZIP(), []int{2}
}

func (x *AddUserInput) GetEmail() string {
	if x != nil {
		return x.Email
	}
	return ""
}

func (x *AddUserInput) GetName() string {
	if x != nil {
		return x.Name
	}
	return ""
}

func (x *AddUserInput) GetSurname() string {
	if x != nil {
		return x.Surname
	}
	return ""
}

func (x *AddUserInput) GetPhoneNumber() string {
	if x != nil {
		return x.PhoneNumber
	}
	return ""
}

func (x *AddUserInput) GetCurrentLocation() string {
	if x != nil {
		return x.CurrentLocation
	}
	return ""
}

type UpdateUserInputSet struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Name            string `protobuf:"bytes,1,opt,name=name,proto3" json:"name,omitempty"`
	Surname         string `protobuf:"bytes,2,opt,name=surname,proto3" json:"surname,omitempty"`
	PhoneNumber     string `protobuf:"bytes,3,opt,name=phoneNumber,proto3" json:"phoneNumber,omitempty"`
	CurrentLocation string `protobuf:"bytes,4,opt,name=currentLocation,proto3" json:"currentLocation,omitempty"`
}

func (x *UpdateUserInputSet) Reset() {
	*x = UpdateUserInputSet{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_internal_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UpdateUserInputSet) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UpdateUserInputSet) ProtoMessage() {}

func (x *UpdateUserInputSet) ProtoReflect() protoreflect.Message {
	mi := &file_proto_internal_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UpdateUserInputSet.ProtoReflect.Descriptor instead.
func (*UpdateUserInputSet) Descriptor() ([]byte, []int) {
	return file_proto_internal_proto_rawDescGZIP(), []int{3}
}

func (x *UpdateUserInputSet) GetName() string {
	if x != nil {
		return x.Name
	}
	return ""
}

func (x *UpdateUserInputSet) GetSurname() string {
	if x != nil {
		return x.Surname
	}
	return ""
}

func (x *UpdateUserInputSet) GetPhoneNumber() string {
	if x != nil {
		return x.PhoneNumber
	}
	return ""
}

func (x *UpdateUserInputSet) GetCurrentLocation() string {
	if x != nil {
		return x.CurrentLocation
	}
	return ""
}

type UpdateUserInput struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Email string              `protobuf:"bytes,1,opt,name=email,proto3" json:"email,omitempty"`
	Set   *UpdateUserInputSet `protobuf:"bytes,2,opt,name=set,proto3" json:"set,omitempty"`
}

func (x *UpdateUserInput) Reset() {
	*x = UpdateUserInput{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_internal_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UpdateUserInput) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UpdateUserInput) ProtoMessage() {}

func (x *UpdateUserInput) ProtoReflect() protoreflect.Message {
	mi := &file_proto_internal_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UpdateUserInput.ProtoReflect.Descriptor instead.
func (*UpdateUserInput) Descriptor() ([]byte, []int) {
	return file_proto_internal_proto_rawDescGZIP(), []int{4}
}

func (x *UpdateUserInput) GetEmail() string {
	if x != nil {
		return x.Email
	}
	return ""
}

func (x *UpdateUserInput) GetSet() *UpdateUserInputSet {
	if x != nil {
		return x.Set
	}
	return nil
}

type WatchUserInput struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Email string `protobuf:"bytes,1,opt,name=email,proto3" json:"email,omitempty"`
}

func (x *WatchUserInput) Reset() {
	*x = WatchUserInput{}
	if protoimpl.UnsafeEnabled {
		mi := &file_proto_internal_proto_msgTypes[5]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *WatchUserInput) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*WatchUserInput) ProtoMessage() {}

func (x *WatchUserInput) ProtoReflect() protoreflect.Message {
	mi := &file_proto_internal_proto_msgTypes[5]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use WatchUserInput.ProtoReflect.Descriptor instead.
func (*WatchUserInput) Descriptor() ([]byte, []int) {
	return file_proto_internal_proto_rawDescGZIP(), []int{5}
}

func (x *WatchUserInput) GetEmail() string {
	if x != nil {
		return x.Email
	}
	return ""
}

var File_proto_internal_proto protoreflect.FileDescriptor

var file_proto_internal_proto_rawDesc = []byte{
	0x0a, 0x14, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c,
	0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x08, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c,
	0x22, 0x24, 0x0a, 0x0c, 0x47, 0x65, 0x74, 0x55, 0x73, 0x65, 0x72, 0x49, 0x6e, 0x70, 0x75, 0x74,
	0x12, 0x14, 0x0a, 0x05, 0x65, 0x6d, 0x61, 0x69, 0x6c, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x05, 0x65, 0x6d, 0x61, 0x69, 0x6c, 0x22, 0x96, 0x01, 0x0a, 0x04, 0x55, 0x73, 0x65, 0x72, 0x12,
	0x14, 0x0a, 0x05, 0x65, 0x6d, 0x61, 0x69, 0x6c, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x05,
	0x65, 0x6d, 0x61, 0x69, 0x6c, 0x12, 0x12, 0x0a, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x18, 0x02, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x12, 0x18, 0x0a, 0x07, 0x73, 0x75, 0x72,
	0x6e, 0x61, 0x6d, 0x65, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x07, 0x73, 0x75, 0x72, 0x6e,
	0x61, 0x6d, 0x65, 0x12, 0x20, 0x0a, 0x0b, 0x70, 0x68, 0x6f, 0x6e, 0x65, 0x4e, 0x75, 0x6d, 0x62,
	0x65, 0x72, 0x18, 0x04, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0b, 0x70, 0x68, 0x6f, 0x6e, 0x65, 0x4e,
	0x75, 0x6d, 0x62, 0x65, 0x72, 0x12, 0x28, 0x0a, 0x0f, 0x63, 0x75, 0x72, 0x72, 0x65, 0x6e, 0x74,
	0x4c, 0x6f, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x18, 0x05, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0f,
	0x63, 0x75, 0x72, 0x72, 0x65, 0x6e, 0x74, 0x4c, 0x6f, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x22,
	0x9e, 0x01, 0x0a, 0x0c, 0x41, 0x64, 0x64, 0x55, 0x73, 0x65, 0x72, 0x49, 0x6e, 0x70, 0x75, 0x74,
	0x12, 0x14, 0x0a, 0x05, 0x65, 0x6d, 0x61, 0x69, 0x6c, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x05, 0x65, 0x6d, 0x61, 0x69, 0x6c, 0x12, 0x12, 0x0a, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x18, 0x02,
	0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x12, 0x18, 0x0a, 0x07, 0x73, 0x75,
	0x72, 0x6e, 0x61, 0x6d, 0x65, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x07, 0x73, 0x75, 0x72,
	0x6e, 0x61, 0x6d, 0x65, 0x12, 0x20, 0x0a, 0x0b, 0x70, 0x68, 0x6f, 0x6e, 0x65, 0x4e, 0x75, 0x6d,
	0x62, 0x65, 0x72, 0x18, 0x04, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0b, 0x70, 0x68, 0x6f, 0x6e, 0x65,
	0x4e, 0x75, 0x6d, 0x62, 0x65, 0x72, 0x12, 0x28, 0x0a, 0x0f, 0x63, 0x75, 0x72, 0x72, 0x65, 0x6e,
	0x74, 0x4c, 0x6f, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x18, 0x05, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x0f, 0x63, 0x75, 0x72, 0x72, 0x65, 0x6e, 0x74, 0x4c, 0x6f, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e,
	0x22, 0x8e, 0x01, 0x0a, 0x12, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x55, 0x73, 0x65, 0x72, 0x49,
	0x6e, 0x70, 0x75, 0x74, 0x53, 0x65, 0x74, 0x12, 0x12, 0x0a, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x18,
	0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x6e, 0x61, 0x6d, 0x65, 0x12, 0x18, 0x0a, 0x07, 0x73,
	0x75, 0x72, 0x6e, 0x61, 0x6d, 0x65, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x07, 0x73, 0x75,
	0x72, 0x6e, 0x61, 0x6d, 0x65, 0x12, 0x20, 0x0a, 0x0b, 0x70, 0x68, 0x6f, 0x6e, 0x65, 0x4e, 0x75,
	0x6d, 0x62, 0x65, 0x72, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0b, 0x70, 0x68, 0x6f, 0x6e,
	0x65, 0x4e, 0x75, 0x6d, 0x62, 0x65, 0x72, 0x12, 0x28, 0x0a, 0x0f, 0x63, 0x75, 0x72, 0x72, 0x65,
	0x6e, 0x74, 0x4c, 0x6f, 0x63, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x18, 0x04, 0x20, 0x01, 0x28, 0x09,
	0x52, 0x0f, 0x63, 0x75, 0x72, 0x72, 0x65, 0x6e, 0x74, 0x4c, 0x6f, 0x63, 0x61, 0x74, 0x69, 0x6f,
	0x6e, 0x22, 0x57, 0x0a, 0x0f, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x55, 0x73, 0x65, 0x72, 0x49,
	0x6e, 0x70, 0x75, 0x74, 0x12, 0x14, 0x0a, 0x05, 0x65, 0x6d, 0x61, 0x69, 0x6c, 0x18, 0x01, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x05, 0x65, 0x6d, 0x61, 0x69, 0x6c, 0x12, 0x2e, 0x0a, 0x03, 0x73, 0x65,
	0x74, 0x18, 0x02, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1c, 0x2e, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e,
	0x61, 0x6c, 0x2e, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x55, 0x73, 0x65, 0x72, 0x49, 0x6e, 0x70,
	0x75, 0x74, 0x53, 0x65, 0x74, 0x52, 0x03, 0x73, 0x65, 0x74, 0x22, 0x26, 0x0a, 0x0e, 0x57, 0x61,
	0x74, 0x63, 0x68, 0x55, 0x73, 0x65, 0x72, 0x49, 0x6e, 0x70, 0x75, 0x74, 0x12, 0x14, 0x0a, 0x05,
	0x65, 0x6d, 0x61, 0x69, 0x6c, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x05, 0x65, 0x6d, 0x61,
	0x69, 0x6c, 0x32, 0xea, 0x01, 0x0a, 0x08, 0x49, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x12,
	0x33, 0x0a, 0x07, 0x47, 0x65, 0x74, 0x55, 0x73, 0x65, 0x72, 0x12, 0x16, 0x2e, 0x69, 0x6e, 0x74,
	0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2e, 0x47, 0x65, 0x74, 0x55, 0x73, 0x65, 0x72, 0x49, 0x6e, 0x70,
	0x75, 0x74, 0x1a, 0x0e, 0x2e, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2e, 0x55, 0x73,
	0x65, 0x72, 0x22, 0x00, 0x12, 0x33, 0x0a, 0x07, 0x41, 0x64, 0x64, 0x55, 0x73, 0x65, 0x72, 0x12,
	0x16, 0x2e, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2e, 0x41, 0x64, 0x64, 0x55, 0x73,
	0x65, 0x72, 0x49, 0x6e, 0x70, 0x75, 0x74, 0x1a, 0x0e, 0x2e, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e,
	0x61, 0x6c, 0x2e, 0x55, 0x73, 0x65, 0x72, 0x22, 0x00, 0x12, 0x39, 0x0a, 0x0a, 0x55, 0x70, 0x64,
	0x61, 0x74, 0x65, 0x55, 0x73, 0x65, 0x72, 0x12, 0x19, 0x2e, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e,
	0x61, 0x6c, 0x2e, 0x55, 0x70, 0x64, 0x61, 0x74, 0x65, 0x55, 0x73, 0x65, 0x72, 0x49, 0x6e, 0x70,
	0x75, 0x74, 0x1a, 0x0e, 0x2e, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2e, 0x55, 0x73,
	0x65, 0x72, 0x22, 0x00, 0x12, 0x39, 0x0a, 0x09, 0x57, 0x61, 0x74, 0x63, 0x68, 0x55, 0x73, 0x65,
	0x72, 0x12, 0x18, 0x2e, 0x69, 0x6e, 0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2e, 0x57, 0x61, 0x74,
	0x63, 0x68, 0x55, 0x73, 0x65, 0x72, 0x49, 0x6e, 0x70, 0x75, 0x74, 0x1a, 0x0e, 0x2e, 0x69, 0x6e,
	0x74, 0x65, 0x72, 0x6e, 0x61, 0x6c, 0x2e, 0x55, 0x73, 0x65, 0x72, 0x22, 0x00, 0x30, 0x01, 0x42,
	0x59, 0x5a, 0x57, 0x68, 0x74, 0x74, 0x70, 0x73, 0x3a, 0x2f, 0x2f, 0x67, 0x69, 0x74, 0x68, 0x75,
	0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x73, 0x61, 0x6c, 0x76, 0x61, 0x74, 0x6f, 0x72, 0x65, 0x2d,
	0x30, 0x38, 0x31, 0x2f, 0x73, 0x61, 0x6c, 0x76, 0x61, 0x74, 0x6f, 0x72, 0x65, 0x65, 0x6d, 0x69,
	0x6c, 0x69, 0x6f, 0x2e, 0x69, 0x74, 0x2f, 0x74, 0x72, 0x65, 0x65, 0x2f, 0x64, 0x65, 0x76, 0x65,
	0x6c, 0x6f, 0x70, 0x6d, 0x65, 0x6e, 0x74, 0x2f, 0x61, 0x70, 0x69, 0x2f, 0x69, 0x6e, 0x74, 0x65,
	0x72, 0x6e, 0x61, 0x6c, 0x2f, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x33,
}

var (
	file_proto_internal_proto_rawDescOnce sync.Once
	file_proto_internal_proto_rawDescData = file_proto_internal_proto_rawDesc
)

func file_proto_internal_proto_rawDescGZIP() []byte {
	file_proto_internal_proto_rawDescOnce.Do(func() {
		file_proto_internal_proto_rawDescData = protoimpl.X.CompressGZIP(file_proto_internal_proto_rawDescData)
	})
	return file_proto_internal_proto_rawDescData
}

var file_proto_internal_proto_msgTypes = make([]protoimpl.MessageInfo, 6)
var file_proto_internal_proto_goTypes = []interface{}{
	(*GetUserInput)(nil),       // 0: internal.GetUserInput
	(*User)(nil),               // 1: internal.User
	(*AddUserInput)(nil),       // 2: internal.AddUserInput
	(*UpdateUserInputSet)(nil), // 3: internal.UpdateUserInputSet
	(*UpdateUserInput)(nil),    // 4: internal.UpdateUserInput
	(*WatchUserInput)(nil),     // 5: internal.WatchUserInput
}
var file_proto_internal_proto_depIdxs = []int32{
	3, // 0: internal.UpdateUserInput.set:type_name -> internal.UpdateUserInputSet
	0, // 1: internal.Internal.GetUser:input_type -> internal.GetUserInput
	2, // 2: internal.Internal.AddUser:input_type -> internal.AddUserInput
	4, // 3: internal.Internal.UpdateUser:input_type -> internal.UpdateUserInput
	5, // 4: internal.Internal.WatchUser:input_type -> internal.WatchUserInput
	1, // 5: internal.Internal.GetUser:output_type -> internal.User
	1, // 6: internal.Internal.AddUser:output_type -> internal.User
	1, // 7: internal.Internal.UpdateUser:output_type -> internal.User
	1, // 8: internal.Internal.WatchUser:output_type -> internal.User
	5, // [5:9] is the sub-list for method output_type
	1, // [1:5] is the sub-list for method input_type
	1, // [1:1] is the sub-list for extension type_name
	1, // [1:1] is the sub-list for extension extendee
	0, // [0:1] is the sub-list for field type_name
}

func init() { file_proto_internal_proto_init() }
func file_proto_internal_proto_init() {
	if File_proto_internal_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_proto_internal_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*GetUserInput); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_internal_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*User); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_internal_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*AddUserInput); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_internal_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UpdateUserInputSet); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_internal_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UpdateUserInput); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_proto_internal_proto_msgTypes[5].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*WatchUserInput); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_proto_internal_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   6,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_proto_internal_proto_goTypes,
		DependencyIndexes: file_proto_internal_proto_depIdxs,
		MessageInfos:      file_proto_internal_proto_msgTypes,
	}.Build()
	File_proto_internal_proto = out.File
	file_proto_internal_proto_rawDesc = nil
	file_proto_internal_proto_goTypes = nil
	file_proto_internal_proto_depIdxs = nil
}