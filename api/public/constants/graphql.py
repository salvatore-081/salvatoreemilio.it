SCHEMA = """type Query {
  getUser(email: String!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User
  updateUser(input: UpdateUserInput!): User
}

type Subscription {
  watchUser(email: String!): User
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
}"""
