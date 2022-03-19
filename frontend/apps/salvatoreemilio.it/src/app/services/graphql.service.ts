import { Injectable } from '@angular/core';
import { ApolloQueryResult, FetchResult } from '@apollo/client/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable } from 'rxjs';
import { User } from '../models/user';

const GET_USER = gql<{ getUser?: User }, { email: string }>`
  query GetUser ($email: String!){
  getUser(email: $email){
    email
    name
    surname
    phoneNumber
    currentLocation
  }
}
`

const WATCH_USER = gql<{ watchUser?: User }, { email: string }>`
  subscription WatchUser ($email: String!){
  watchUser(email: $email){
    email
    name
    surname
    phoneNumber
    currentLocation
  }
}
`

@Injectable({
  providedIn: 'root'
})
export class GraphqlService {

  constructor(private apollo: Apollo) { }

  getUser(email: string): Observable<ApolloQueryResult<{ getUser?: User }>> {
    return this.apollo.query({
      query: GET_USER,
      variables: {
        email: email
      }
    })
  }

  watchUser(email: string): Observable<FetchResult<{ watchUser?: User | undefined; }, Record<string, any>, Record<string, any>>> {
    return this.apollo.subscribe({
      query: WATCH_USER,
      variables: {
        email: email
      }
    })
  }
}
