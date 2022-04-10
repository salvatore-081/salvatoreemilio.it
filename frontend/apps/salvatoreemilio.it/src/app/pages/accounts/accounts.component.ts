import { Component, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { Observable, take } from 'rxjs';
import { AccountsStore, AccountsUser } from './accounts.store';

@Component({
  selector: 'accounts',
  templateUrl: './accounts.component.html',
  styleUrls: ['./accounts.component.scss'],
  providers: [AccountsStore],
})
export class AccountsComponent implements OnInit {
  loading$: Observable<boolean> = this.accountsStore.loading$.pipe(take(2));
  userList$: Observable<AccountsUser[]> = this.accountsStore.userList$;

  constructor(
    private accountsStore: AccountsStore,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {}

  selectAccount($email: string): void {
    this.accountsStore.selectUser($email);
  }

  switchAccount($email: string, name?: string): void {
    this.messageService.add({
      severity: 'success',
      summary: `Ciao, ${name ?? $email}!`,
    });
    this.accountsStore.switchCurrentAccount($email);
  }
}
