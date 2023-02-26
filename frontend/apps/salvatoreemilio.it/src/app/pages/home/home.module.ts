import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home.component';
import { HomeRoutingModule } from './home-routing.module';
import { LetModule } from '@ngrx/component';
import { TerminalComponent } from '../../components/terminal/terminal.component';
import { SkeletonModule } from 'primeng/skeleton';
import { ProjectCardComponent } from '../../components/project-card/project-card.component';

const PRIMENG_MODULES = [SkeletonModule];

const STANDALONE_COMPONENTS = [ProjectCardComponent, TerminalComponent];

@NgModule({
  declarations: [HomeComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    LetModule,
    ...PRIMENG_MODULES,
    ...STANDALONE_COMPONENTS,
  ],
})
export class HomeModule {}
