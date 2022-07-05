SCHEMA = """
  scalar Base64

  type Query {
    getUserList: GetUserListOutput
    getUser(email: String!): User
    getProjects(email: String!): GetProjectsOutput
  }

  type Mutation {
    login(input: LoginInput!): LoginResponse
    logout(refresh_token: String!): LogoutResponse
    updateUser(input: UpdateUserInput!): User
    addProject(input: AddProjectInput!): Project
    updateProject(input: UpdateProjectInput!): Project
    deleteProject(id: String!): DeleteProjectOutput
  }

  type Subscription {
    watchUser(email: String!): User
    watchProjects(email: String!): ProjectFeed
  }

  input LoginInput {
    email: String!
    password: String!
    totp: String
  }

  input AddProjectInput {
    email: String!
    title: String!
    description: String
    image: Base64
    tags: [String]
    links: [AddLinkInput]
  }

  input AddLinkInput {
    name: String!
    url: String!
  }

  input UpdateProjectInput {
    id: String!
    payload: UpdateProjectInputPayload!
  }

  input UpdateProjectInputPayload {
    email: String
    title: String
    description: String
    image: Base64
    tags: [String]
    links: [AddLinkInput]
    index: Int
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

  type GetProjectsOutput {
    projects: [Project]
  }

  type Project {
    id: String!
    email: String!
    title: String!
    description: String
    image: Base64
    tags: [String]
    links: [Link]
    index: Int!
  }

  type ProjectFeed {
    new_val: Project
    old_val: Project
  }

  type DeleteProjectOutput {
    id: String!
  }

  type Link {
    name: String
    url: String
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
