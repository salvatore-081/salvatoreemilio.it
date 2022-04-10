import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Store } from "@ngrx/store";
import { finalize, Observable } from "rxjs";
import { LOADER_OFF, LOADER_ON } from "../state/actions/loader.actions";

@Injectable()
export class LoaderInterceptor implements HttpInterceptor {

  constructor(private store: Store) { }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    this.store.dispatch(LOADER_ON({ key: request.url }))

    return next.handle(request).pipe(finalize(() => this.store.dispatch(LOADER_OFF({ key: request.url }))));
  }
}