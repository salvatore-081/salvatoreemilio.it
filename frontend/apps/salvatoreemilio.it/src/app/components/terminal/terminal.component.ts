import { Component, OnDestroy, OnInit } from '@angular/core';
import { TerminalService } from 'primeng/terminal';
import { first, map, Observable, Subject, takeUntil } from 'rxjs';
import { User } from '../../models';
import { RestService } from '../../services/rest.service';
import { TerminalStore } from './terminal.store';

@Component({
  selector: 'terminal',
  templateUrl: './terminal.component.html',
  styleUrls: ['./terminal.component.scss'],
  providers: [TerminalService, TerminalStore],
})
export class TerminalComponent implements OnInit, OnDestroy {
  destroy$: Subject<void> = new Subject<void>();
  user$: Observable<User> = this.terminalStore.selectUser$;
  ip$: Observable<string> = this.restService.getWhatsMyIp();
  readonly COMMANDS: Map<string, { value: Function; description: string }> =
    new Map<string, { value: Function; description: string }>([
      ['HELP', { value: () => this.commandHelp(), description: '' }],
      [
        'USER.NAME',
        {
          value: () => this.commandUserName(),
          description: 'display user name',
        },
      ],
      [
        'USER.EMAIL',
        {
          value: () => this.commandUserEmail(),
          description: 'display user email',
        },
      ],
    ]);
  readonly COMMANDS_LIST: string = Array.from(this.COMMANDS.keys())
    .filter((k) => k !== 'HELP')
    .map((v) => `${v.toLowerCase()} - ${this.COMMANDS.get(v)?.description}`)
    .reduce((prev, curr) => {
      if (prev === '') {
        return curr;
      }
      return `${prev}\n${curr}`;
    }, '');

  constructor(
    private terminalStore: TerminalStore,
    private restService: RestService,
    private terminalService: TerminalService
  ) {}

  ngOnInit(): void {
    this.terminalService.commandHandler
      .pipe(takeUntil(this.destroy$))
      .subscribe((command: string) => {
        const F: Function | undefined = this.COMMANDS.get(
          command.toUpperCase()
        )?.value;
        if (F) {
          console.log('F', F);
          F();
        } else {
          this.terminalService.sendResponse(
            `${command}: command not found. Type 'help' to list available commands`
          );
        }
      });
    // this.user$.subscribe((v) => console.log('user', v));
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  commandHelp(): void {
    this.terminalService.sendResponse(this.COMMANDS_LIST);
    return;
  }

  commandUserName(): void {
    this.user$
      .pipe(
        map((v) => v.name ?? ''),
        first()
      )
      .subscribe((v) => this.terminalService.sendResponse(v));
  }

  commandUserEmail(): void {
    this.user$
      .pipe(
        map((v) => v.email),
        first()
      )
      .subscribe((v) => this.terminalService.sendResponse(v));
  }
}
