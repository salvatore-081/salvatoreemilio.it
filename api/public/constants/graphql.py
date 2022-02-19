from gql import gql

SCHEMA = """
  type Query {
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
  }
"""


GET_USER = gql(
    """
    query getUser($email: String!){
        getUser(email: $email){
            email
            name
            surname
            phoneNumber
            currentLocation
        }
    }
    """
)

ADD_USER = gql(
    """
    mutation addUser($input: AddUserInput!){
      addUser(input: $input){
        email
        name
        surname
        phoneNumber
        currentLocation
      }
    }
    """
)
