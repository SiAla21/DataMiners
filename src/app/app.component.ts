import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {RecommenderComponent} from './recommender/recommender.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, RecommenderComponent], // 👈 Obligatoire pour ngModel
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  postText = '';
  clubName = '';

  getRecommendation() {
    console.log('Texte:', this.postText, 'Club:', this.clubName);
    // Ajouter l’appel HTTP ici si nécessaire
  }
}
