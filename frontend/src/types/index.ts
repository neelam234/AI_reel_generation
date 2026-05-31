export interface Project {
  id: string;
  title: string;
  status: 'created' | 'processing' | 'completed' | 'failed';
  reference_video?: string;
  product_images: string[];
  output_video?: string;
  created_at: string;
}

export interface CreateProjectRequest {
  title: string;
}
