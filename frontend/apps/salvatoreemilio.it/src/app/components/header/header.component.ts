import { Component, OnInit } from '@angular/core';
import { NavigationEnd, NavigationStart, Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { MenuItem } from 'primeng/api';
import { Observable } from 'rxjs';
import { SELECT_LOADER_LOADING } from '../../app.state';
import { HeaderStore } from './header.store';
import { LOADER_OFF, LOADER_ON } from '../../state/actions/loader.actions';
import { ProgressBarModule } from 'primeng/progressbar';
import { SkeletonModule } from 'primeng/skeleton';
import { AvatarModule } from 'primeng/avatar';
import { MenuModule } from 'primeng/menu';
import { CommonModule } from '@angular/common';
import { LetModule } from '@ngrx/component';
import { ButtonModule } from 'primeng/button';

const NG_MODULES = [
  ProgressBarModule,
  SkeletonModule,
  AvatarModule,
  MenuModule,
  ButtonModule,
];

@Component({
  selector: 'header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  providers: [HeaderStore],
  standalone: true,
  imports: [CommonModule, LetModule, ...NG_MODULES],
})
export class HeaderComponent implements OnInit {
  homePageRoute: boolean = true;

  items: MenuItem[] = [
    {
      label: 'Manage account',
      icon: 'pi pi-user-edit',
      command: () => this.router.navigate(['/account']),
    },
    {
      label: 'Switch account',
      icon: 'pi pi-users',
      command: () => {
        this.router.navigate(['/accounts']);
      },
    },
  ];

  profilePicture$: Observable<string | undefined> =
    this.headerStore.profilePicture$;
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
