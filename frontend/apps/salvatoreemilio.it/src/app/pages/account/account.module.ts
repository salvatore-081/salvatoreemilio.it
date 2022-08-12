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
import { ProjectCardModule } from '../../components/project-card/project-card.module';
import { BlockUIModule } from 'primeng/blockui';
import { PanelModule } from 'primeng/panel';
import { ConfirmDialogComponent } from './dialogs/confirm-dialog/confirm-dialog.component';

const MODULES = [ProjectCardModule];

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
  BlockUIModule,
  PanelModule,
];

@NgModule({
  declarations: [
    AccountComponent,
    AddProjectDialogComponent,
    ConfirmDialogComponent,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    AccountRoutingModule,
    ReactiveComponentModule,
    ...PRIMENG_MODULES,
    ...MODULES,
  ],
})
export class AccountModule {}
