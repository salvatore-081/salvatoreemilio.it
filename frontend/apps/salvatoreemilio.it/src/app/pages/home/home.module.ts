import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home.component';
import { HomeRoutingModule } from './home-routing.module';
import { LetModule } from '@ngrx/component';
import { TerminalComponent } from '../../components/terminal/terminal.component';
import { TerminalModule } from 'primeng/terminal';
import { SkeletonModule } from 'primeng/skeleton';
import { ProjectCardModule } from '../../components/project-card/project-card.module';

const PRIMENG_MODULES = [TerminalModule, SkeletonModule];

const MODULES = [ProjectCardModule];

@NgModule({
  declarations: [HomeComponent, TerminalComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    LetModule,
    ...PRIMENG_MODULES,
    ...MODULES,
  ],
})
export class HomeModule {}
