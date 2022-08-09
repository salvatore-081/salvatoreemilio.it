import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { DialogService } from 'primeng/dynamicdialog';
import { FileUpload } from 'primeng/fileupload';
import { Observable, tap } from 'rxjs';
import { Project } from '../../models';
import { AccountStore } from './account.store';
import { AddProjectDialogComponent } from './dialogs/add-project-dialog/add-project-dialog.component';

@Component({
  selector: 'account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.scss'],
  providers: [AccountStore, DialogService],
})
export class AccountComponent implements OnInit {
  profilePictureMaxFileSize: number = 1;

  email$: Observable<string> = this.accountStore.email$;
  emailLoading$: Observable<boolean> = this.accountStore.emailLoading$;

  nameFormControl: FormControl = new FormControl('', [
    Validators.pattern(`^[A-zÀ-ú][A-zÀ-ú ]{2,}$`),
  ]);
  name$: Observable<string | undefined> = this.accountStore.name$;
  nameLoading$: Observable<boolean> = this.accountStore.nameLoading$.pipe(
    tap((v) =>
      v ? this.nameFormControl.disable() : this.nameFormControl.enable()
    )
  );

  surnameFormControl: FormControl = new FormControl('', [
    Validators.pattern(`^[A-zÀ-ú][A-zÀ-ú ]{2,}$`),
  ]);
  surname$: Observable<string | undefined> = this.accountStore.surname$;
  surnameLoading$: Observable<boolean> = this.accountStore.surnameLoading$.pipe(
    tap((v) =>
      v ? this.surnameFormControl.disable() : this.surnameFormControl.enable()
    )
  );

  phoneNumberFormControl: FormControl = new FormControl('', [
    Validators.pattern(`^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$`),
  ]);
  phoneNumber$: Observable<string | undefined> = this.accountStore.phoneNumber$;
  phoneNumberLoading$: Observable<boolean> =
    this.accountStore.phoneNumberLoading$.pipe(
      tap((v) =>
        v
          ? this.phoneNumberFormControl.disable()
          : this.phoneNumberFormControl.enable()
      )
    );

  locationFormControl: FormControl = new FormControl('', [
    Validators.minLength(2),
  ]);
  location$: Observable<string | undefined> = this.accountStore.location$;
  locationLoading$: Observable<boolean> =
    this.accountStore.locationLoading$.pipe(
      tap((v) =>
        v
          ? this.locationFormControl.disable()
          : this.locationFormControl.enable()
      )
    );

  profilePictureFormControl: FormControl = new FormControl('');
  profilePicture$: Observable<string | undefined> =
    this.accountStore.profilePicture$;
  profilePictureLoading$: Observable<boolean> =
    this.accountStore.profilePictureLoading$.pipe(
      tap((v) =>
        v
          ? this.profilePictureFormControl.disable()
          : this.profilePictureFormControl.enable()
      )
    );

  projects: Observable<Project[]> = this.accountStore.projects$;

  constructor(
    private accountStore: AccountStore,
    private dialogService: DialogService
  ) {}

  ngOnInit(): void {
    this.name$.subscribe((v) => this.nameFormControl.patchValue(v));
    this.surname$.subscribe((v) => this.surnameFormControl.patchValue(v));
    this.phoneNumber$.subscribe((v) =>
      this.phoneNumberFormControl.patchValue(v)
    );
    this.location$.subscribe((v) => this.locationFormControl.patchValue(v));
    this.profilePicture$.subscribe((v) =>
      this.profilePictureFormControl.patchValue(v)
    );
  }

  updateName(): void {
    this.accountStore.updateName(this.nameFormControl.value);
    this.nameFormControl.markAsPristine();
  }

  updateSurname(): void {
    this.accountStore.updateSurname(this.surnameFormControl.value);
    this.surnameFormControl.markAsPristine();
  }

  updatePhoneNumber(): void {
    this.accountStore.updatePhoneNumber(this.phoneNumberFormControl.value);
    this.phoneNumberFormControl.markAsPristine();
  }

  updateLocation(): void {
    this.accountStore.updateLocation(this.locationFormControl.value);
    this.locationFormControl.markAsPristine();
  }

  updateProfilePicture($event: any, fileUpload: FileUpload) {
    this.accountStore.updateProfilePicture(
      $event.files[0]?.objectURL?.changingThisBreaksApplicationSecurity
    );
    fileUpload.clear();
  }

  openAddProjectDialog(): void {
    this.dialogService.open(AddProjectDialogComponent, {
      styleClass: 'add-project-dialog',
      header: 'Add project',
    });
  }
}
