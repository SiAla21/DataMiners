import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import {ClubComponent} from '../club/club.component';


@Component({
  selector: 'app-ronaldo-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule, RouterModule,ClubComponent], // 👈 AJOUT ICI
  templateUrl: './recommender.component.html',
  styleUrls: ['./recommender.component.css'],

})

export class RecommenderComponent {
  llmProfile: string = '';
  llmConditions: any[] = [];
  profile = '';
  conditions: any[] = [];

  postText = '';
  clubName: string = 'Juventus'; // ← Valeur fixée ici
  results: any[] = [];
  resultKeys: string[] = []
  tried = false;


  constructor(private http: HttpClient) {}

  getRecommendation() {
    const payload = {
      text: this.postText,
      club: this.clubName
    };

    this.http.post<any>('http://127.0.0.1:5000/recommend', payload).subscribe({
      next: (data) => {
        console.log("✅ Résultats reçus :", data);
        this.results = data.results;
        this.resultKeys = this.results.length > 0 ? Object.keys(this.results[0]) : [];
        this.llmProfile = data.profile;
        this.llmConditions = data.conditions;
      },
      error: (err) => {
        console.error("❌ Erreur lors de l'appel à l'API :", err);
        this.results = [];
        this.resultKeys = [];
        this.tried = true;
      }
    });
  }}
