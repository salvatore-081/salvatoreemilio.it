import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { environment } from '../environments/environment';
import { LOAD } from './state/actions/user.actions';

@Component({
  selector: 'frontend-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  constructor(private store: Store) { }

  ngOnInit(): void {
    this.store.dispatch(LOAD({ email: environment.email }))
  }

}
