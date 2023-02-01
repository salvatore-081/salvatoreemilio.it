import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccountComponent } from './account.component';
import { AccountRoutingModule } from './account-routing.module';
import { SkeletonModule } from 'primeng/skeleton';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { LetModule } from '@ngrx/component';
import { ReactiveFormsModule } from '@angular/forms';
import { ToastModule } from 'primeng/toast';
import { FileUploadModule } from 'primeng/fileupload';
import { DynamicDialogModule } from 'primeng/dynamicdialog';
import { ChipsModule } from 'primeng/chips';
import { TableModule } from 'primeng/table';
import { BlockUIModule } from 'primeng/blockui';
import { PanelModule } from 'primeng/panel';
import { ConfirmDialogComponent } from './dialogs/confirm-dialog/confirm-dialog.component';
import { ProjectCardComponent } from '../../components/project-card/project-card.component';
import { ProjectDialogComponent } from './dialogs/project-dialog/project-dialog.component';

const PRIMENG_MODULES = [
  SkeletonModule,
  InputTextModule,
  AvatarModule,
  ButtonModule,
  FileUploadModule,
  ToastModule,
  DynamicDialogModule,
  ChipsModule,
  TableModule,
  BlockUIModule,
  PanelModule,
];

const STANDALONE_COMPONENTS = [
  ProjectCardComponent,
  ConfirmDialogComponent,
  ProjectDialogComponent,
];

@NgModule({
  declarations: [AccountComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    AccountRoutingModule,
    LetModule,
    ...PRIMENG_MODULES,
    ...STANDALONE_COMPONENTS,
  ],
})
export class AccountModule {}
