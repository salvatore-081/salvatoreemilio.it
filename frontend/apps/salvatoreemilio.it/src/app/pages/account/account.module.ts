import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccountComponent } from './account.component';
import { AccountRoutingModule } from './account-routing.module';
import { SkeletonModule } from 'primeng/skeleton';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ReactiveComponentModule } from '@ngrx/component';
import { ReactiveFormsModule } from '@angular/forms';
import { ToastModule } from 'primeng/toast';
import { FileUploadModule } from 'primeng/fileupload';

const PRIMENG_MODULES = [
  SkeletonModule,
  InputTextModule,
  AvatarModule,
  FileUploadModule,
  ButtonModule,
  ToastModule,
];

@NgModule({
  declarations: [AccountComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    AccountRoutingModule,
    ReactiveComponentModule,
    PRIMENG_MODULES,
  ],
})
export class AccountModule {}
