import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Auth } from './auth';

export interface Case {
  id: number;
  title: string;
  description: string | null;
  status: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class Cases {
  private apiUrl = 'http://127.0.0.1:8001';

  constructor(private http: HttpClient, private auth: Auth) {}

  private authHeaders() {
    return { Authorization: `Bearer ${this.auth.getToken()}` };
  }

  list(): Observable<Case[]> {
    return this.http.get<Case[]>(`${this.apiUrl}/cases`, { headers: this.authHeaders() });
  }
}