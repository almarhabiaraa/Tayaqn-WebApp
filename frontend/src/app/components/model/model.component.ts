import { Component } from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {ApiService} from "../../services/api.service";

@Component({
  selector: 'app-model',
  templateUrl: './model.component.html',
  styleUrls: ['./model.component.scss']
})
export class ModelComponent {
  selectedFile: File | null = null;
  uploadProgress: number | null = null;
  uploadStatus: 'idle' | 'uploading' | 'success' | 'error' = 'idle';
  errorMessage = '';
  successMessage = '';
  isAdmin = false;

  constructor(
    private apiService: ApiService,
    private authService: AuthService
  ) {
    this.isAdmin = this.authService.getRole() === 'ADMIN';
  }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
    this.uploadStatus = 'idle';
  }

  onSubmit(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Please select a CSV file first';
      return;
    }

    this.uploadStatus = 'uploading';
    this.errorMessage = '';
    this.successMessage = '';

    this.apiService.trainModel(this.selectedFile).subscribe({
      next: (event: any) => {
        if (event.type === 1 && event.loaded && event.total) {
          this.uploadProgress = Math.round((event.loaded / event.total) * 100);
        }
      },
      error: (error) => {
        this.uploadStatus = 'error';
        this.errorMessage = error.error?.detail || 'Training failed. Please check the file format.';
        console.error('Training error:', error);
      },
      complete: () => {
        this.uploadStatus = 'success';
        this.successMessage = 'Model training completed successfully!';
        this.selectedFile = null;
        this.uploadProgress = null;
      }
    });
  }

  requiredColumns = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
    'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
    'HvyAlcoholConsump', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk',
    'Sex', 'Age', 'prediction'
  ];
  isDragging = false;

  // Add this method
  onFileDropped(files: FileList): void {
    if (files.length > 0) {
      this.selectedFile = files[0];
      this.uploadStatus = 'idle';
    }
  }
}
