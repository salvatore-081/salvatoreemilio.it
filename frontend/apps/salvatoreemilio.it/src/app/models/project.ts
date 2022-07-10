export interface GetProjectsOutput {
  projects: Project[] | undefined;
}

export interface Project {
  id: string;
  email: string;
  title: string;
  description?: string;
  image?: string;
  tags?: string[];
  links?: Link[];
  index: number;
}

export interface Link {
  name: string;
  url: string;
}

export interface ProjectFeed {
  new_val?: Project;
  old_val?: Project;
}
