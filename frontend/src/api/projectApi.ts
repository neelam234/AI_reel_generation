import axios from 'axios';
import type { Project, CreateProjectRequest } from '../types';

const API_BASE_URL = 'http://localhost:8001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const projectApi = {
  createProject: async (data: CreateProjectRequest): Promise<Project> => {
    const response = await api.post('/projects/', data);
    return response.data;
  },
  getProject: async (id: string): Promise<Project> => {
    const response = await api.get(`/projects/${id}`);
    return response.data;
  },
  uploadReference: async (id: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/projects/${id}/upload-reference`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  uploadImages: async (id: string, files: File[]) => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    return api.post(`/projects/${id}/upload-images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  generateReel: async (id: string) => {
    return api.post(`/projects/${id}/generate`);
  },
};
