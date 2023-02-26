import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { DividerModule } from 'primeng/divider';
import { AccountsUser } from '../../pages/accounts/accounts.store';

const PRIMENG_MODULES = [AvatarModule, DividerModule, ButtonModule];
@Component({
  selector: 'account-card',
  templateUrl: './account-card.component.html',
  styleUrls: ['./account-card.component.scss'],
  standalone: true,
  imports: [CommonModule, ...PRIMENG_MODULES],
})
export class AccountCardComponent implements OnInit {
  @Input() user: AccountsUser = {
    email: '',
    selected: false,
    current: false,
  };

  @Output() selectAccount: EventEmitter<string> = new EventEmitter<string>();
  @Output() switchCurrentAccount: EventEmitter<string> =
    new EventEmitter<string>();

  constructor(private router: Router) {}

  ngOnInit(): void {}

  selectUser(): void {
    if (!this.user.selected) {
      this.selectAccount.emit(this.user.email);
    }
  }

  switchAccount(): void {
    this.switchCurrentAccount.emit(this.user.email);
  }

  navigateToAccount(): void {
    this.router.navigate(['account']);
  }
}
