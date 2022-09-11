import { Component, Input, OnInit } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngrx/store';
import { SELECT_USER_EMAIL } from 'apps/salvatoreemilio.it/src/app/app.state';
import { GraphqlService } from 'apps/salvatoreemilio.it/src/app/services/graphql.service';
import { UtilsService } from 'apps/salvatoreemilio.it/src/app/services/utils.service';
import { MessageService } from 'primeng/api';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';
import { FileUpload } from 'primeng/fileupload';
import { first, switchMap, take } from 'rxjs';

@Component({
  templateUrl: './project-dialog.component.html',
  styleUrls: ['./project-dialog.component.scss'],
})
export class ProjectDialogComponent implements OnInit {
  update: boolean = false;

  projectFormGroup: FormGroup = new FormGroup({
    id: new FormControl(''),
    title: new FormControl('', [Validators.required, Validators.minLength(3)]),
    description: new FormControl(''),
    image: new FormControl(''),
    tags: new FormControl([]),
    links: new FormControl([]),
  });

  linkFormGroup: FormGroup = new FormGroup({
    name: new FormControl('', [Validators.required, Validators.minLength(1)]),
    url: new FormControl('', [
      Validators.required,
      Validators.pattern(
        /^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/
      ),
    ]),
  });

  submitButtonDisabled: boolean = false;
  constructor(
    public ref: DynamicDialogRef,
    private utilsService: UtilsService,
    private messageService: MessageService,
    private graphqlService: GraphqlService,
    private store: Store,
    public config: DynamicDialogConfig
  ) {}

  ngOnInit(): void {
    if (this.config?.data?.project) {
      this.update = true;
      this.projectFormGroup.patchValue({
        id: this.config.data.project.id,
        title: this.config.data.project.title,
        description: this.config.data.project?.description ?? '',
        image: this.config.data.project?.image ?? '',
        tags: this.config.data.project?.tags ?? [],
        links: [...this.config.data.project?.links] ?? [],
      });
    }
  }

  updateProject(): void {
    this.submitButtonDisabled = true;
    this.graphqlService
      .updateProject({
        id: this.projectFormGroup.controls['id'].value,
        payload: {
          ...(this.projectFormGroup.controls['title'].dirty
            ? {
                title: this.projectFormGroup.controls['title'].value,
              }
            : {}),
          ...(this.projectFormGroup.controls['description'].dirty
            ? {
                description:
                  this.projectFormGroup.controls['description'].value,
              }
            : {}),
          ...(this.projectFormGroup.controls['image'].dirty
            ? { image: this.projectFormGroup.controls['image'].value }
            : {}),
          ...(this.projectFormGroup.controls['tags'].dirty
            ? { tags: this.projectFormGroup.controls['tags'].value }
            : {}),
          ...(this.projectFormGroup.controls['links'].dirty
            ? { links: this.projectFormGroup.controls['links'].value }
            : {}),
        },
      })
      .pipe(first())
      .subscribe({
        next: (next) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Project updated!',
          });
          this.ref.close();
        },
        error: (error) => {
          console.error('updateProject error', error);
          this.messageService.add({
            severity: 'error',
            summary: 'Ops... qualcosa è andato storto!',
          });
          this.submitButtonDisabled = false;
        },
      });
  }

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
        name: this.linkFormGroup.controls['name'].value,
        url: this.linkFormGroup.controls['url'].value,
      },
    ]);
    this.projectFormGroup.controls['links'].markAsDirty();
    this.linkFormGroup.controls['name'].reset();
    this.linkFormGroup.controls['url'].reset();
  }

  deleteLink(index: number): void {
    this.projectFormGroup.controls['links'].value.splice(index, 1);
    this.projectFormGroup.controls['links'].markAsDirty();
  }
}
