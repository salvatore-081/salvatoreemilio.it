export interface User {
  email: string;
  name?: string;
  surname?: string;
  phoneNumber?: string;
  location?: string;
  profilePicture?: string;
}

export interface UserListItem {
  email: string;
  name?: string;
  surname?: string;
  profilePicutre?: string;
}
