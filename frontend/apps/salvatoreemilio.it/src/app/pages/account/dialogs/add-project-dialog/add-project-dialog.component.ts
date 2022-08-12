import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { SELECT_USER_EMAIL } from 'apps/salvatoreemilio.it/src/app/app.state';
import { GraphqlService } from 'apps/salvatoreemilio.it/src/app/services/graphql.service';
import { UtilsService } from 'apps/salvatoreemilio.it/src/app/services/utils.service';
import { MessageService } from 'primeng/api';
import { DynamicDialogRef } from 'primeng/dynamicdialog';
import { FileUpload } from 'primeng/fileupload';
import { first, switchMap, take } from 'rxjs';

@Component({
  templateUrl: './add-project-dialog.component.html',
  styleUrls: ['./add-project-dialog.component.scss'],
})
export class AddProjectDialogComponent {
  projectFormGroup: FormGroup = new FormGroup({
    title: new FormControl('', [Validators.required, Validators.minLength(3)]),
    description: new FormControl(''),
    image: new FormControl(''),
    tags: new FormControl([]),
    links: new FormControl([]),
    newLinkName: new FormControl(''),
    newLinkURL: new FormControl(''),
  });
  submitButtonDisabled: boolean = false;
  constructor(
    public ref: DynamicDialogRef,
    private utilsService: UtilsService,
    private messageService: MessageService,
    private graphqlService: GraphqlService,
    private store: Store
  ) {}

  addProject(): void {
    this.submitButtonDisabled = true;
    this.store
      .select(SELECT_USER_EMAIL)
      .pipe(
        take(1),
        switchMap((email: string) =>
          this.graphqlService.addProject({
            email: email,
            title: this.projectFormGroup.controls['title'].value,
            description: this.projectFormGroup.controls['description'].value,
            image: this.projectFormGroup.controls['image'].value,
            tags: this.projectFormGroup.controls['tags'].value,
            links: this.projectFormGroup.controls['links'].value,
          })
        ),
        first()
      )
      .subscribe({
        next: (next) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Project added!',
          });
          this.ref.close();
        },
        error: (error) => {
          console.error('addProject error', error);
          this.messageService.add({
            severity: 'error',
            summary: 'Ops... qualcosa è andato storto!',
          });
          this.submitButtonDisabled = false;
        },
      });
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
    this.projectFormGroup.controls['links'].patchValue([
      ...this.projectFormGroup.controls['links'].value,
      {
        name: this.projectFormGroup.controls['newLinkName'].value,
        url: this.projectFormGroup.controls['newLinkURL'].value,
      },
    ]);
    this.projectFormGroup.controls['newLinkName'].reset();
    this.projectFormGroup.controls['newLinkURL'].reset();
  }

  deleteLink(index: number): void {
    this.projectFormGroup.controls['links'].value.splice(index, 1);
  }
}
