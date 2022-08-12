import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProjectCardComponent } from './project-card.component';

// const PRIMENG_MODULES = [];

@NgModule({
  declarations: [ProjectCardComponent],
  imports: [
    CommonModule,
    //  ...PRIMENG_MODULES
  ],
  exports: [ProjectCardComponent],
})
export class ProjectCardModule {}
