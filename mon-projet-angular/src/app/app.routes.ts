import { Routes } from '@angular/router';
import { RecommenderComponent } from './recommender/recommender.component';
import { RonaldoProfileComponent } from './ronaldo-profile/ronaldo-profile.component'; // ✅ Import

export const routes: Routes = [
  { path: '', redirectTo: 'recommender', pathMatch: 'full' }, // ✅ redirection par défaut
  { path: 'recommender', component: RecommenderComponent },
  { path: 'ronaldo', component: RonaldoProfileComponent } // ✅ nouvelle route ajoutée
];
