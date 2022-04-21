import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home.component';
import { HomeRoutingModule } from './home-routing.module';
import { ReactiveComponentModule } from '@ngrx/component';
import { TerminalComponent } from '../../components/terminal/terminal.component';
import { TerminalModule } from 'primeng/terminal';
import { SkeletonModule } from 'primeng/skeleton';

const PRIMENG_MODULES = [TerminalModule, SkeletonModule];
@NgModule({
  declarations: [HomeComponent, TerminalComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    ReactiveComponentModule,
    ...PRIMENG_MODULES,
  ],
})
export class HomeModule {}
