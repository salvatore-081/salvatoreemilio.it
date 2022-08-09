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
import { DynamicDialogModule } from 'primeng/dynamicdialog';
import { AddProjectDialogComponent } from './dialogs/add-project-dialog/add-project-dialog.component';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ChipsModule } from 'primeng/chips';
import { TableModule } from 'primeng/table';

const PRIMENG_MODULES = [
  TableModule,
  SkeletonModule,
  InputTextModule,
  InputTextareaModule,
  AvatarModule,
  FileUploadModule,
  ButtonModule,
  ToastModule,
  DynamicDialogModule,
  ChipsModule,
  TableModule,
];

@NgModule({
  declarations: [AccountComponent, AddProjectDialogComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    AccountRoutingModule,
    ReactiveComponentModule,
    PRIMENG_MODULES,
  ],
})
export class AccountModule {}
