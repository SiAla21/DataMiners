import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import {ClubComponent} from './club/club.component'; // ✔️ seul import nécessaire ici

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, RouterOutlet, ClubComponent], // ✔️ supprimer les composants inutilisés ici
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  postText = '';
  clubName = '';

  getRecommendation() {
    console.log('Texte:', this.postText, 'Club:', this.clubName);
    // Tu peux ici déclencher un service HTTP pour les recommandations
  }
}
