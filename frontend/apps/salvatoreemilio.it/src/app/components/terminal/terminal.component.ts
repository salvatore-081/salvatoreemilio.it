import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { LetModule } from '@ngrx/component';
import { SkeletonModule } from 'primeng/skeleton';
import { TerminalModule, TerminalService } from 'primeng/terminal';
import { first, map, Observable, Subject, takeUntil } from 'rxjs';
import { User } from '../../models';
import { RestService } from '../../services/rest.service';
import { TerminalStore } from './terminal.store';

const PRIMENG_MODULES = [SkeletonModule, TerminalModule];
@Component({
  selector: 'terminal',
  templateUrl: './terminal.component.html',
  styleUrls: ['./terminal.component.scss'],
  providers: [TerminalService, TerminalStore],
  standalone: true,
  imports: [CommonModule, LetModule, ...PRIMENG_MODULES],
})
export class TerminalComponent implements OnInit, OnDestroy {
  destroy$: Subject<void> = new Subject<void>();
  user$: Observable<User> = this.terminalStore.selectUser$;
  ip$: Observable<string> = this.restService.getWhatsMyIp();
  readonly COMMANDS: Map<string, { value: Function; description: string }> =
    new Map<string, { value: Function; description: string }>([
      ['HELP', { value: () => this.commandHelp(), description: '' }],
      [
        'NAME',
        {
          value: () => this.commandUserName(),
          description: 'display name',
        },
      ],
      [
        'EMAIL',
        {
          value: () => this.commandUserEmail(),
          description: 'display email',
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
          F();
        } else {
          this.terminalService.sendResponse(
            `${command}: command not found. Type 'help' to list available commands`
          );
        }
      });
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
