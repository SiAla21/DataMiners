import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// ✅ Define and export interfaces
export interface ClubDetails {
  club: string;
  [key: string]: any;
}

export interface WeaknessResponse {
  club: string;
  top_5_weakest_positions: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ClubService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  getClubDetails(club: string): Observable<ClubDetails> {
    return this.http.get<ClubDetails>(`${this.baseUrl}/club-details/${encodeURIComponent(club)}`);
  }

  getWeakestPositions(club: string): Observable<WeaknessResponse> {
    return this.http.get<WeaknessResponse>(`${this.baseUrl}/predict/${encodeURIComponent(club)}`);
  }
}
