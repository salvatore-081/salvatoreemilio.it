from gql import gql

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
