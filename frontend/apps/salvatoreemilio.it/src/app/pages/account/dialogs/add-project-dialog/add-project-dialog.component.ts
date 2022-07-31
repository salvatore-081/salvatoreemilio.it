import { Component } from '@angular/core';
import { DialogService } from 'primeng/dynamicdialog';

@Component({
  templateUrl: './add-project-dialog.component.html',
  styleUrls: ['./add-project-dialog.component.scss'],
  providers: [DialogService],
})
export class AddProjectDialogComponent {
  constructor(public dialogService: DialogService) {}
}
