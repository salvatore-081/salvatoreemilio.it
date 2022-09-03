import { Component, Input, OnInit } from '@angular/core';
import { Project, ProjectTag } from '../../models';
import { UtilsService } from '../../services/utils.service';

@Component({
  selector: 'project-card',
  templateUrl: './project-card.component.html',
  styleUrls: ['./project-card.component.scss'],
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
