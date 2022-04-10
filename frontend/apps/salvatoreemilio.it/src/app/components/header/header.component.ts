import { Component, OnInit } from '@angular/core';
import { NavigationEnd, NavigationStart, Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { MenuItem } from 'primeng/api';
import { Observable } from 'rxjs';
import { User } from '../../models';
import { SELECT_LOADER_LOADING } from '../../app.state';
import { HeaderStore } from './header.store';
import { LOADER_OFF, LOADER_ON } from '../../state/actions/loader.actions';

@Component({
  selector: 'header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  providers: [HeaderStore],
})
export class HeaderComponent implements OnInit {
  homePageRoute: boolean = true;

  items: MenuItem[] = [
    {
      label: 'Gestisci Account',
      icon: 'pi pi-user-edit',
      command: () => this.router.navigate(['/account']),
    },
    {
      label: 'Cambia Account',
      icon: 'pi pi-users',
      command: () => {
        this.router.navigate(['/accounts']);
      },
    },
  ];

  selectedUser$: Observable<User> = this.headerStore.selectedUser$;
  loader$: Observable<boolean> = this.store.select(SELECT_LOADER_LOADING);

  constructor(
    private readonly headerStore: HeaderStore,
    private store: Store,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.router.events.subscribe((event: any) => {
      if (event instanceof NavigationStart) {
        this.store.dispatch(LOADER_ON({ key: `NAVIGATION ${event.url}` }));
      }
      if (event instanceof NavigationEnd) {
        this.homePageRoute = event.url.includes('home') || event.url === '/';
        this.store.dispatch(LOADER_OFF({ key: `NAVIGATION ${event.url}` }));
      }
    });
  }

  navigateHome(): void {
    this.router.navigate(['home']);
  }
}
