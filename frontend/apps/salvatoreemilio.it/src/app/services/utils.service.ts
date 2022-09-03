import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, switchMap } from 'rxjs';
import * as CONSTANTS from '../app.constants';
import { ProjectTag } from '../models';

@Injectable({
  providedIn: 'root',
})
export class UtilsService {
  constructor(private httpClient: HttpClient) {}

  readBlob(url: string): Observable<string> {
    let readerSubject = new Subject<string>();
    return this.httpClient.get(url, { responseType: 'blob' }).pipe(
      switchMap((blob: Blob) => {
        const fileReader: FileReader = new FileReader();
        fileReader.readAsDataURL(blob);
        fileReader.onload = (ev: ProgressEvent<FileReader>) => {
          readerSubject.next((ev.target?.result as string)?.split(',', 2)[1]);
          readerSubject.complete();
        };
        return readerSubject.asObservable();
      })
    );
  }

  getProjectTagInfo(key: string, size: string): ProjectTag | undefined {
    let info: ProjectTag | undefined = CONSTANTS.PROJECT_TAGS.get(
      key.toLowerCase().replace(/\./g, '-')
    );

    if (!info) {
      return undefined;
    }

    return { ...info, iconClass: `custom-icon ${size} ${info.iconClass}` };
  }
}
