import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TooltipModule } from 'primeng/tooltip';
import { Project, ProjectTag } from '../../models';
import { UtilsService } from '../../services/utils.service';

const PRIMENG_MODULES = [TooltipModule, ButtonModule];

@Component({
  selector: 'project-card',
  templateUrl: './project-card.component.html',
  styleUrls: ['./project-card.component.scss'],
  standalone: true,
  imports: [CommonModule, ...PRIMENG_MODULES],
})
export class ProjectCardComponent implements OnInit {
  @Input() project: Project | undefined = undefined;

  constructor(private utils: UtilsService) {}

  ngOnInit(): void {}

  getProjectTagInfo(key: string, size: string): ProjectTag | undefined {
    return this.utils.getProjectTagInfo(key, size);
  }

  goToUrl(url: string): void {
    window.open(url, '_blank');
  }
}
