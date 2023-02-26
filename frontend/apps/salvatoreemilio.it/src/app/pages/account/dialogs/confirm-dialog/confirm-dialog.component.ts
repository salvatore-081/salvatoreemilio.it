import { Component, OnInit } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';

const PRIMENG_MODULES = [ButtonModule];
@Component({
  templateUrl: './confirm-dialog.component.html',
  styleUrls: ['./confirm-dialog.component.scss'],
  standalone: true,
  imports: [...PRIMENG_MODULES],
})
export class ConfirmDialogComponent implements OnInit {
  label: string = '';

  constructor(
    public ref: DynamicDialogRef,
    public config: DynamicDialogConfig
  ) {}

  ngOnInit(): void {
    this.label = this.config.data?.label;
  }

  closeDialog(result: boolean): void {
    this.ref.close(result);
  }
}
