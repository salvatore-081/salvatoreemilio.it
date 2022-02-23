SCHEMA = """
  type Query {
    getUser(email: String!): User
  }

  type Mutation {
    login(input: LoginInput!): LoginResponse
    createUser(input: CreateUserInput!): User
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

  input CreateUserInput {
    email: String!
    name: String
    surname: String
    phoneNumber: String
    currentLocation: String
  }

  input UpdateUserInput {
    email: String!
    set: UpdateUserInputSet!
  }

  input UpdateUserInputSet {
    name: String
    surname: String
    phoneNumber: String
    currentLocation: String
  }

  type User {
    email: String!
    name: String
    surname: String
    phoneNumber: String
    currentLocation: String
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
"""
