SCHEMA = """
  scalar Base64

  type Query {
    getUserList: GetUserListOutput
    getUser(email: String!): User
  }

  type Mutation {
    login(input: LoginInput!): LoginResponse
    logout(refresh_token: String!): LogoutResponse
    updateUser(input: UpdateUserInput!): User
  }

  type Subscription {
    watchUser(email: String!): User
  }

  input LoginInput {
    email: String!
    password: String!
    totp: String
  }

  input UpdateUserInput {
    email: String!
    payload: UpdateUserInputPayload!
  }

  input UpdateUserInputPayload {
    name: String
    surname: String
    phoneNumber: String
    location: String
    profilePicture: Base64
  }

  type UserListItem {
    email: String!
    name: String
    surname: String
    profilePicture: Base64
  }

  type GetUserListOutput {
    userList: [UserListItem]
  }

  type User {
    email: String!
    name: String
    surname: String
    phoneNumber: String
    location: String
    profilePicture: Base64
  }

  type LoginResponse {
    access_token: String
    expires_in: Int
    refresh_expires_in: Int
    refresh_token: String
    token_type: String
    session_state: String
    scope: String
  }

  type LogoutResponse {
    refresh_token: String
  }
"""
