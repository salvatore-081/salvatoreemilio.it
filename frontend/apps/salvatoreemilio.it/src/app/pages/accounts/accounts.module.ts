import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccountsComponent } from './accounts.component';
import { AccountsRoutingModule } from './accounts-routing.module';
import { CardModule } from 'primeng/card';
import { SkeletonModule } from 'primeng/skeleton';
import { AvatarModule } from 'primeng/avatar';
import { AccountCardComponent } from '../../components/account-card/account-card.component';
import { DividerModule } from 'primeng/divider';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';

const PRIMENG_MODULES = [
  CardModule,
  SkeletonModule,
  AvatarModule,
  DividerModule,
  ButtonModule,
  ToastModule,
];

@NgModule({
  declarations: [AccountsComponent, AccountCardComponent],
  imports: [CommonModule, AccountsRoutingModule, PRIMENG_MODULES],
})
export class AccountsModule {}
