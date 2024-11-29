import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://localhost:8000'; // URL du backend FastAPI

  constructor(private http: HttpClient) {}

  // Endpoint pour uploader un fichier
  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(`${this.baseUrl}/upload/`, formData);
  }

  // Endpoint pour poser une question
  askQuestion(file: File, question: string): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
  
    const queryParams = `?question=${encodeURIComponent(question)}`;
    return this.http.post(`${this.baseUrl}/ask-question/${queryParams}`, formData);
  }
  
}
