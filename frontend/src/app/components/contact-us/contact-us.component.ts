// contact-us.component.ts
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {ApiService} from "../../services/api.service";


@Component({
  selector: 'app-contact-us',
  templateUrl: './contact-us.component.html',
  styleUrls: ['./contact-us.component.scss']
})
export class ContactUsComponent {
  contactForm: FormGroup;
  isLoading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {
    this.contactForm = this.fb.group({
      subject: ['', Validators.required],
      message: ['', [Validators.required, Validators.minLength(20)]]
    });
  }

  onSubmit(): void {
    if (this.contactForm.invalid) return;

    this.isLoading = true;
    this.successMessage = '';
    this.errorMessage = '';

    const formData = {
      subject: this.contactForm.value.subject,
      message: this.contactForm.value.message
    };

    this.apiService.sendMessage(formData).subscribe({
      next: () => {
        this.successMessage = 'Your message has been sent successfully!';
        this.contactForm.reset();
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to send message. Please try again later.';
        console.error('Contact form error:', error);
        this.isLoading = false;
      }
    });
  }
}
