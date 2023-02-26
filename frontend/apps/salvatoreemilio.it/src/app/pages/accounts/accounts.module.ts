import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccountsComponent } from './accounts.component';
import { AccountsRoutingModule } from './accounts-routing.module';
import { CardModule } from 'primeng/card';
import { SkeletonModule } from 'primeng/skeleton';
import { AvatarModule } from 'primeng/avatar';
import { DividerModule } from 'primeng/divider';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { AccountCardComponent } from '../../components/account-card/account-card.component';

const PRIMENG_MODULES = [
  CardModule,
  SkeletonModule,
  AvatarModule,
  DividerModule,
  ButtonModule,
  ToastModule,
];

const STANDALONE_COMPONENTS = [AccountCardComponent];

@NgModule({
  declarations: [AccountsComponent],
  imports: [
    CommonModule,
    AccountsRoutingModule,
    ...PRIMENG_MODULES,
    ...STANDALONE_COMPONENTS,
  ],
})
export class AccountsModule {}
