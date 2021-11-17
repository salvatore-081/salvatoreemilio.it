package models

type CreateUserInput struct {
	Email           string  `json:"email,omitempty"`
	Name            *string `json:"name,omitempty"`
	Surname         *string `json:"surname,omitempty"`
	PhoneNumber     *string `json:"phoneNumber,omitempty"`
	CurrentLocation *string `json:"currentLocation,omitempty"`
}

type UpdateUserInput struct {
	Email string              `json:"email,omitempty"`
	Set   *UpdateUserInputSet `json:"set,omitempty"`
}

type UpdateUserInputSet struct {
	Name            *string `json:"name,omitempty"`
	Surname         *string `json:"surname,omitempty"`
	PhoneNumber     *string `json:"phoneNumber,omitempty"`
	CurrentLocation *string `json:"currentLocation,omitempty"`
}

type User struct {
	Email           string  `json:"email,omitempty"`
	Name            *string `json:"name,omitempty"`
	Surname         *string `json:"surname,omitempty"`
	PhoneNumber     *string `json:"phoneNumber,omitempty"`
	CurrentLocation *string `json:"currentLocation,omitempty"`
}

type WatchUserFeed struct {
	NewVal *User `json:"new_val,omitempty"`
	OldVal *User `json:"old_val,omitempty"`
}
