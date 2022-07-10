import { Injectable } from '@angular/core';
import { ApolloQueryResult, FetchResult } from '@apollo/client/core';
import { Apollo, gql, MutationResult } from 'apollo-angular';
import { Observable } from 'rxjs';
import { ProjectFeed } from '../models';
import { User, UserListItem } from '../models/user';

const GET_USER_LIST = gql<
  { getUserList?: { userList?: UserListItem[] } },
  undefined
>`
  query GetUserList {
    getUserList {
      userList {
        email
        name
        surname
        profilePicture
      }
    }
  }
`;

const WATCH_USER = gql<{ watchUser?: User }, { email: string }>`
  subscription WatchUser($email: String!) {
    watchUser(email: $email) {
      email
      name
      surname
      phoneNumber
      location
      profilePicture
    }
  }
`;

const UPDATE_USER_NAME = gql<{ user: User }, { email: string; name: string }>`
  mutation UpdateUserName($email: String!, $name: String) {
    updateUser(input: { email: $email, payload: { name: $name } }) {
      name
    }
  }
`;

const UPDATE_USER_SURNAME = gql<
  { user: User },
  { email: string; surname: string }
>`
  mutation UpdateSurname($email: String!, $surname: String) {
    updateUser(input: { email: $email, payload: { surname: $surname } }) {
      surname
    }
  }
`;

const UPDATE_USER_PHONE_NUMBER = gql<
  { user: User },
  { email: string; phoneNumber: string }
>`
  mutation UpdatePhoneNumber($email: String!, $phoneNumber: String) {
    updateUser(
      input: { email: $email, payload: { phoneNumber: $phoneNumber } }
    ) {
      name
    }
  }
`;

const UPDATE_USER_LOCATION = gql<
  { user: User },
  { email: string; location: string }
>`
  mutation UpdateUserLocation($email: String!, $location: String) {
    updateUser(input: { email: $email, payload: { location: $location } }) {
      name
    }
  }
`;

const UPDATE_USER_PROFILE_PICTURE = gql<
  { user: User },
  { email: string; profilePicture: string }
>`
  mutation UpdateProfilePicture($email: String!, $profilePicture: Base64) {
    updateUser(
      input: { email: $email, payload: { profilePicture: $profilePicture } }
    ) {
      profilePicture
    }
  }
`;

const WATCH_PROJECTS = gql<{ projectFeed: any }, { email: string }>`
  subscription WatchProjects($email: String!) {
    watchProjects(email: $email) {
      old_val {
        id
        email
        title
        description
        image
        tags
        links {
          name
          url
        }
        index
      }
      new_val {
        id
        email
        title
        description
        image
        tags
        links {
          name
          url
        }
        index
      }
    }
  }
`;

@Injectable({
  providedIn: 'root',
})
export class GraphqlService {
  constructor(private apollo: Apollo) {}

  getUserList(): Observable<
    ApolloQueryResult<{ getUserList?: { userList?: UserListItem[] } }>
  > {
    return this.apollo.query({
      query: GET_USER_LIST,
      fetchPolicy: 'network-only',
    });
  }

  updateUserName(
    email: string,
    name: string
  ): Observable<MutationResult<{ user: User }>> {
    return this.apollo.mutate({
      mutation: UPDATE_USER_NAME,
      variables: {
        email: email,
        name: name,
      },
    });
  }

  updateUserSurname(
    email: string,
    surname: string
  ): Observable<MutationResult<{ user: User }>> {
    return this.apollo.mutate({
      mutation: UPDATE_USER_SURNAME,
      variables: {
        email: email,
        surname: surname,
      },
    });
  }

  updateUserPhoneNumber(
    email: string,
    phoneNumber: string
  ): Observable<MutationResult<{ user: User }>> {
    return this.apollo.mutate({
      mutation: UPDATE_USER_PHONE_NUMBER,
      variables: {
        email: email,
        phoneNumber: phoneNumber,
      },
    });
  }

  updateUserLocation(
    email: string,
    location: string
  ): Observable<MutationResult<{ user: User }>> {
    return this.apollo.mutate({
      mutation: UPDATE_USER_LOCATION,
      variables: {
        email: email,
        location: location,
      },
    });
  }

  updateUserProfilePicture(
    email: string,
    profilePicture: string
  ): Observable<MutationResult<{ user: User }>> {
    return this.apollo.mutate({
      mutation: UPDATE_USER_PROFILE_PICTURE,
      variables: {
        email: email,
        profilePicture: profilePicture,
      },
    });
  }

  watchUser(
    email: string
  ): Observable<
    FetchResult<
      { watchUser?: User | undefined },
      Record<string, any>,
      Record<string, any>
    >
  > {
    return this.apollo.subscribe({
      query: WATCH_USER,
      variables: {
        email: email,
      },
    });
  }

  watchProjects(
    email: string
  ): Observable<FetchResult<{ projectFeed?: ProjectFeed | undefined }>> {
    return this.apollo.subscribe({
      query: WATCH_PROJECTS,
      variables: {
        email: email,
      },
    });
  }
}
