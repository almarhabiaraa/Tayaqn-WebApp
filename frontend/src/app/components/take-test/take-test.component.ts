// take-test.component.ts
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { Router } from '@angular/router';
import { AuthService } from "../../services/auth.service";
import { ApiService } from "../../services/api.service";

@Component({
  selector: 'app-take-test',
  templateUrl: './take-test.component.html',
  styleUrls: ['./take-test.component.scss']
})
export class TakeTestComponent {
  testForm: FormGroup;
  isAdmin = false;
  isLoading = false;
  errorMessage = '';

  // Step navigation
  currentStep: number = 0;
  totalSteps: number = 6;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router
  ) {
    this.isAdmin = this.authService.getRole() === 'ADMIN';

    this.testForm = this.fb.group({
      full_name: [''],  // Only for admin
      high_bp: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      high_chol: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      chol_check: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      bmi: [null, [Validators.required, Validators.min(10), Validators.max(100)]],
      smoker: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      stroke: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      heart_disease: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      phys_activity: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      fruits: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      veggies: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      hvy_alcohol: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      gen_hlth: [null, [Validators.required, Validators.min(1), Validators.max(5)]],
      ment_hlth: [null, [Validators.required, Validators.min(0), Validators.max(30)]],
      phys_hlth: [null, [Validators.required, Validators.min(0), Validators.max(30)]],
      diff_walk: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      sex: [null, [Validators.required, Validators.min(0), Validators.max(1)]],
      age: [null, [Validators.required, Validators.min(1), Validators.max(13)]]
    });

    if (!this.isAdmin) {
      this.testForm.get('full_name')?.disable();
    }
  }

  // Navigation methods
  nextStep(): void {
    if (this.currentStep < this.totalSteps - 1) {
      this.currentStep++;
    }
  }

  prevStep(): void {
    if (this.currentStep > 0) {
      this.currentStep--;
    }
  }

  onSubmit(): void {
    if (this.testForm.invalid) {
      this.errorMessage = 'Please fill all required fields correctly';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const formData = this.testForm.value;
    if (!this.isAdmin) {
      delete formData.full_name;
    }

    this.apiService.submitTest(formData).subscribe({
      next: () => {
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        this.errorMessage = 'An error occurred. Please try again.';
        console.error('Submission error:', error);
        this.isLoading = false;
      },
      complete: () => this.isLoading = false
    });
  }
}
