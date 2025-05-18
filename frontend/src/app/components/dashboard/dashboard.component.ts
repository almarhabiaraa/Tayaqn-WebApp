import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {ApiService} from "../../services/api.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  historicalData: any[] = [];
  expandedRow: number | null = null;
  isAdmin = false;
  connectedUser: any;

  constructor(
    private apiService: ApiService,
    public authService: AuthService
  ) { }

  ngOnInit(): void {
    this.isAdmin = this.authService.getRole() === 'ADMIN';
    this.profile();
    this.loadHistory();
  }

  loadHistory(): void {
    this.apiService.getHistory().subscribe({
      next: (data) => {
        this.historicalData = data;
      },
      error: (error) => {
        console.error('Error fetching history:', error);
      }
    });
  }

  profile(){
    this.apiService.profile().subscribe({
      next: (data) => {
        this.connectedUser = data;
      },
      error: (error) => {
        console.error('Error fetching profile:', error);
      }
    });
  }
  getObjectKeys(obj: any): string[] {
    return Object.keys(obj).filter(key =>
      !['id', 'user_id', 'timestamp', 'prediction'].includes(key)
    );
  }

  toggleRow(index: number): void {
    this.expandedRow = this.expandedRow === index ? null : index;
  }
}
