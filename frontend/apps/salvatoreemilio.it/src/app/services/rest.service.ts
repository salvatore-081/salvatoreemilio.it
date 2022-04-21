import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { finalize, map, Observable, of, tap } from 'rxjs';
import { environment } from '../../environments/environment';

interface WathsMyIpCache {
  value: string;
  expires: Date;
}

@Injectable({
  providedIn: 'root',
})
export class RestService {
  readonly BASE_URL: string = environment.rest.url;

  private readonly WATHS_MY_IP_CACHE_DURATION: number = 60 * 60000;
  private whatsMyIpCache: WathsMyIpCache | undefined = undefined;

  constructor(private httpClient: HttpClient) {}

  getWhatsMyIp(): Observable<string> {
    const ENDPOINT: string = `${this.BASE_URL}/misc/whatsmyip`;

    const CACHED: string | undefined = this.getWhatsMyIpCacheValue();

    if (CACHED) {
      return of(CACHED);
    }

    return this.httpClient.get<{ ip: string }>(ENDPOINT).pipe(
      map((v) => v.ip),
      tap(
        (ip: string) =>
          (this.whatsMyIpCache = {
            value: ip,
            expires: new Date(
              new Date().getTime() + this.WATHS_MY_IP_CACHE_DURATION
            ),
          })
      )
    );
  }

  private getWhatsMyIpCacheValue(): string | undefined {
    if (!this.whatsMyIpCache) {
      return undefined;
    }

    if (this.whatsMyIpCache.expires.getTime() <= new Date().getTime()) {
      this.whatsMyIpCache = undefined;
      return undefined;
    }
    return this.whatsMyIpCache.value;
  }
}
