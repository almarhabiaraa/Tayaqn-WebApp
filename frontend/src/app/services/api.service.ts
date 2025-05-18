import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:8001/api';

  constructor(
    private http: HttpClient
  ) { }

  profile(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/me`);
  }

  submitTest(data: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/predict`, data);
  }

  getHistory(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/history`);
  }

  trainModel(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(`${this.apiUrl}/train`, formData, {
      reportProgress: true,
      observe: 'events'
    });
  }

  sendMessage(formData: { subject: any; message: any }) {
    return this.http.post(`${this.apiUrl}/contact`, formData);
  }
}
