import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Link } from 'apps/salvatoreemilio.it/src/app/models';
import { UtilsService } from 'apps/salvatoreemilio.it/src/app/services/utils.service';
import { DialogService } from 'primeng/dynamicdialog';
import { FileUpload } from 'primeng/fileupload';

@Component({
  templateUrl: './add-project-dialog.component.html',
  styleUrls: ['./add-project-dialog.component.scss'],
  providers: [DialogService],
})
export class AddProjectDialogComponent {
  links: Link[] = [
    {
      name: 'name',
      url: 'url',
    },
    {
      name: 'nam2e',
      url: 'ur2l',
    },
  ];

  projectFormGroup: FormGroup = new FormGroup({
    title: new FormControl('', [Validators.required, Validators.minLength(3)]),
    description: new FormControl('', [
      Validators.required,
      Validators.minLength(3),
    ]),
    image: new FormControl(''),
    tags: new FormControl([]),
    newLinkName: new FormControl(''),
    newLinkURL: new FormControl(''),
  });
  constructor(
    public dialogService: DialogService,
    private utilsService: UtilsService
  ) {}

  addProject(): void {
    console.log('AddProjectDialogComponent addProject()');
    console.log(this.projectFormGroup.value);
  }

  addImage($event: any, fileUpload: FileUpload): void {
    this.utilsService
      .readBlob(
        $event.files[0]?.objectURL?.changingThisBreaksApplicationSecurity
      )
      .subscribe((v) => {
        this.projectFormGroup.controls['image'].setValue(v);
        fileUpload.clear();
      });
  }

  addLink(): void {
    this.links.push({
      name: this.projectFormGroup.controls['newLinkName'].value,
      url: this.projectFormGroup.controls['newLinkURL'].value,
    });
    this.projectFormGroup.controls['newLinkName'].reset();
    this.projectFormGroup.controls['newLinkURL'].reset();
  }

  deleteLink(index: number): void {
    this.links.splice(index, 1);
  }
}
