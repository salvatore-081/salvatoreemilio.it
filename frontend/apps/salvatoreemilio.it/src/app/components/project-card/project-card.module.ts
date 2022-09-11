import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProjectCardComponent } from './project-card.component';
import { TooltipModule } from 'primeng/tooltip';
import { ButtonModule } from 'primeng/button';

const PRIMENG_MODULES = [TooltipModule, ButtonModule];

@NgModule({
  declarations: [ProjectCardComponent],
  imports: [CommonModule, ...PRIMENG_MODULES],
  exports: [ProjectCardComponent],
})
export class ProjectCardModule {}
