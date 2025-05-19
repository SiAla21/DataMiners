import { Injectable } from '@angular/core';
import {HttpClient, HttpEvent, HttpHeaders, HttpParams, HttpRequest} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {


  private baseUrl = 'http://localhost:8081/api/users';

  private apiUrl = 'http://localhost:8081/api/users';
  constructor(private http: HttpClient) {}

  /**
   * Sends 3 player images and name to verify the player
   * @param playerId - ID of the player
   * @param playerName - Name of the player (used to search on Flashscore)
   * @param images - Array of exactly 3 File objects
   */
  uploadImage(file: File) {
    const formData = new FormData();
    formData.append('image', file);
    return this.http.post<string>('http://localhost:8081/api/users/upload', formData, { responseType: 'text' as 'json' });
  }

  verifyPlayer(playerId: number, name: string, imagePaths: string[]) {
    const params = new HttpParams()
      .set('playerName', name)
      .appendAll({ images: imagePaths });
    return this.http.post('http://localhost:8081/api/users/verify-player/' + playerId, null, { params, responseType: 'text' });
  }

  deleteImage(path: string) {
    return this.http.post('http://localhost:8081/api/users/delete', { path }, { responseType: 'text' as 'json' });
  }
}
